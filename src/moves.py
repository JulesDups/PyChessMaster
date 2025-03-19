def is_valid_move(board, start_row, start_col, end_row, end_col, white_turn, last_pawn_double_move, castling_rights):
    piece = board[start_row][start_col]
    target = board[end_row][end_col]

    if not is_valid_target(piece, target):
        return False

    # Additional validation: Check if the move is physically valid
    valid_move = False
    if piece.lower() == 'k':  # King
        valid_move = is_valid_king_move(board, start_row, start_col, end_row, end_col, white_turn, castling_rights)
    elif piece.lower() == 'p':  # Pawn
        valid_move = is_valid_pawn_move(board, start_row, start_col, end_row, end_col, white_turn, last_pawn_double_move)
    elif piece.lower() == 'q':  # Queen
        valid_move = is_valid_queen_move(board, start_row, start_col, end_row, end_col)
    elif piece.lower() == 'n':  # Knight
        valid_move = is_valid_knight_move(start_row, start_col, end_row, end_col)
    elif piece.lower() == 'b':  # Bishop
        valid_move = is_valid_bishop_move(board, start_row, start_col, end_row, end_col)
    elif piece.lower() == 'r':  # Rook
        valid_move = is_valid_rook_move(board, start_row, start_col, end_row, end_col)
    
    if not valid_move:
        return False
    
    # Check if the move puts the player's own king in check
    temp_board = [row[:] for row in board]
    
    # Special handling for castling - need to move both king and rook
    castling_move = False
    if piece.lower() == 'k' and abs(end_col - start_col) == 2:
        castling_move = True
        temp_board[end_row][end_col] = temp_board[start_row][start_col]
        temp_board[start_row][start_col] = ' '
        
        # Move the rook as well
        if end_col > start_col:  # Kingside castling
            temp_board[end_row][5] = temp_board[end_row][7]
            temp_board[end_row][7] = ' '
        else:  # Queenside castling
            temp_board[end_row][3] = temp_board[end_row][0]
            temp_board[end_row][0] = ' '
    else:
        # Standard move
        temp_board[end_row][end_col] = temp_board[start_row][start_col]
        temp_board[start_row][start_col] = ' '
    
    # Check for en passant capture
    if piece.lower() == 'p' and start_col != end_col and board[end_row][end_col] == ' ' and last_pawn_double_move == (start_row, end_col):
        temp_board[last_pawn_double_move[0]][last_pawn_double_move[1]] = ' '
        
    if is_king_in_check(temp_board, white_turn):
        return False
        
    return True

def is_valid_target(piece, target):
    # Check if the target square is valid for the piece
    return target == ' ' or (piece.isupper() != target.isupper())

def is_valid_king_move(board, start_row, start_col, end_row, end_col, white_turn, castling_rights):
    # Add debug printing
    print(f"King move check: {start_row},{start_col} to {end_row},{end_col}")
    
    # Standard king move - one square in any direction
    if abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1:
        return True
    
    # Castling - must be in the same row
    if start_row == end_row and abs(end_col - start_col) == 2:
        castling_valid = is_valid_castling(board, start_row, start_col, end_col, white_turn, castling_rights)
        print(f"Castling check result: {castling_valid}")
        return castling_valid
    
    return False

def is_valid_castling(board, start_row, start_col, end_col, white_turn, castling_rights):
    # Add debug printing
    print(f"Checking castling: {start_row},{start_col} to {start_row},{end_col}")
    print(f"Castling rights: {castling_rights}")
    
    # If castling_rights is None, castling is not allowed
    if castling_rights is None:
        print("Castling rights are None")
        return False
        
    # Use the appropriate side based on player's turn
    side = "white" if white_turn else "black"
    
    # Check if the side exists in castling_rights
    if side not in castling_rights:
        print(f"Side {side} not in castling rights")
        return False
    
    # Check if kingside castling
    if end_col == 6:
        print("Checking kingside castling")
        if 'kingside' not in castling_rights[side]:
            print("Kingside castling right not found")
            return False
            
        # Check if the king has already moved
        if not castling_rights[side]['kingside']:
            print("Kingside castling right is False")
            return False
            
        result = check_castling_conditions(board, start_row, start_col, 7, 1, 2, side, 
                                        castling_rights[side]['kingside'], white_turn)
        print(f"Kingside castling check result: {result}")
        return result
        
    # Check if queenside castling
    elif end_col == 2:
        print("Checking queenside castling")
        if 'queenside' not in castling_rights[side]:
            print("Queenside castling right not found")
            return False
            
        # Check if the king has already moved
        if not castling_rights[side]['queenside']:
            print("Queenside castling right is False")
            return False
            
        result = check_castling_conditions(board, start_row, start_col, 0, -1, -2, side, 
                                        castling_rights[side]['queenside'], white_turn)
        print(f"Queenside castling check result: {result}")
        return result
        
    return False

def check_castling_conditions(board, row, king_col, rook_col, step1, step2, side, castling_right, white_turn):
    print(f"Checking castling conditions: row={row}, king_col={king_col}, rook_col={rook_col}")
    print(f"Path step1={step1}, step2={step2}")
    
    # Check if castling rights are enabled
    if not castling_right:
        print("Castling right is False")
        return False
        
    # Check if the rook is in the correct position
    if board[row][rook_col].lower() != 'r':
        print(f"No rook at position {row},{rook_col}: found {board[row][rook_col]}")
        return False
        
    # Check if the path is clear
    if step1 > 0:  # Kingside
        if board[row][king_col + 1] != ' ' or board[row][king_col + 2] != ' ':
            print(f"Path not clear: {board[row][king_col + 1]}, {board[row][king_col + 2]}")
            return False
    else:  # Queenside
        if board[row][king_col - 1] != ' ' or board[row][king_col - 2] != ' ' or board[row][king_col - 3] != ' ':
            print(f"Path not clear: {board[row][king_col - 1]}, {board[row][king_col - 2]}, {board[row][king_col - 3]}")
            return False
    
    # Check if king is in check in current, intermediate, or final position
    if is_king_in_check(board, white_turn):
        print("King is currently in check")
        return False
        
    # Check if king passes through check
    if is_king_in_check(board, white_turn, king_pos=(row, king_col + step1)):
        print(f"King would pass through check at {row},{king_col + step1}")
        return False
        
    # Check if king's destination would be in check
    dest_col = king_col + 2 if step1 > 0 else king_col - 2
    if is_king_in_check(board, white_turn, king_pos=(row, dest_col)):
        print(f"King would end in check at {row},{dest_col}")
        return False
        
    print("All castling conditions passed!")
    return True

def is_valid_pawn_move(board, start_row, start_col, end_row, end_col, white_turn, last_pawn_double_move):
    direction = -1 if white_turn else 1
    start_row_limit = 6 if white_turn else 1
    if start_col == end_col and board[end_row][end_col] == ' ':
        if end_row == start_row + direction:
            return True
        if start_row == start_row_limit and end_row == start_row + 2 * direction and board[start_row + direction][start_col] == ' ':
            return True
    if abs(end_col - start_col) == 1:
        return is_valid_pawn_capture(board, start_row, start_col, end_row, end_col, white_turn, last_pawn_double_move)
    return False

def is_valid_pawn_capture(board, start_row, start_col, end_row, end_col, white_turn, last_pawn_double_move):
    direction = -1 if white_turn else 1
    if end_row == start_row + direction and board[end_row][end_col] != ' ':
        return True
    if end_row == start_row + direction and last_pawn_double_move == (start_row, end_col):
        return is_valid_en_passant(board, start_row, start_col, end_row, end_col, last_pawn_double_move, white_turn)
    return False

def is_valid_en_passant(board, start_row, start_col, end_row, end_col, last_pawn_double_move, white_turn):
    temp_board = [row[:] for row in board]
    temp_board[end_row][end_col] = temp_board[start_row][start_col]
    temp_board[start_row][start_col] = ' '
    temp_board[last_pawn_double_move[0]][last_pawn_double_move[1]] = ' '
    return not is_king_in_check(temp_board, white_turn)

def is_valid_queen_move(board, start_row, start_col, end_row, end_col):
    # Queen moves like rook or bishop
    is_rook_like = (start_row == end_row or start_col == end_col)
    is_bishop_like = (abs(start_row - end_row) == abs(start_col - end_col))
    
    # Check if the move is valid and path is clear
    return (is_rook_like or is_bishop_like) and is_path_clear(board, start_row, start_col, end_row, end_col)

def is_valid_knight_move(start_row, start_col, end_row, end_col):
    return (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]

def is_valid_bishop_move(board, start_row, start_col, end_row, end_col):
    return abs(start_row - end_row) == abs(start_col - end_col) and is_path_clear(board, start_row, start_col, end_row, end_col)

def is_valid_rook_move(board, start_row, start_col, end_row, end_col):
    return (start_row == end_row or start_col == end_col) and is_path_clear(board, start_row, start_col, end_row, end_col)

def is_path_clear(board, start_row, start_col, end_row, end_col):
    # Helper function to check if the path between start and end is clear
    row_step = (end_row - start_row) // max(1, abs(end_row - start_row)) if start_row != end_row else 0
    col_step = (end_col - start_col) // max(1, abs(end_col - start_col)) if start_col != end_col else 0
    current_row, current_col = start_row + row_step, start_col + col_step
    while (current_row, current_col) != (end_row, end_col):
        if board[current_row][current_col] != ' ':
            return False
        current_row += row_step
        current_col += col_step
    return True

def is_king_in_check(board, white_turn, king_pos=None, castling_rights=None):
    # Ensure `board` is a list of rows
    if not isinstance(board, list) or not all(isinstance(row, list) for row in board):
        raise ValueError("Invalid board structure passed to is_king_in_check")
    
    # Find king position if not provided
    if king_pos is None:
        for r in range(8):
            for c in range(8):
                if board[r][c] == ('K' if white_turn else 'k'):
                    king_pos = (r, c)
                    break
            if king_pos:
                break
    
    if king_pos is None:  # If king_pos is still None, return False (king not on board)
        return False

    # Check if any opponent's piece can attack the king
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            # Check only opponent's pieces
            if piece != ' ' and ((piece.islower() and white_turn) or (piece.isupper() and not white_turn)):
                # Use piece-specific move validity to avoid infinite recursion
                if piece.lower() == 'p':  # Pawn
                    if is_valid_pawn_capture(board, r, c, king_pos[0], king_pos[1], not white_turn, None):
                        return True
                elif piece.lower() == 'n':  # Knight
                    if is_valid_knight_move(r, c, king_pos[0], king_pos[1]):
                        return True
                elif piece.lower() == 'b':  # Bishop
                    if is_valid_bishop_move(board, r, c, king_pos[0], king_pos[1]):
                        return True
                elif piece.lower() == 'r':  # Rook
                    if is_valid_rook_move(board, r, c, king_pos[0], king_pos[1]):
                        return True
                elif piece.lower() == 'q':  # Queen
                    if is_valid_queen_move(board, r, c, king_pos[0], king_pos[1]):
                        return True
                elif piece.lower() == 'k':  # King (can be one square away)
                    if abs(r - king_pos[0]) <= 1 and abs(c - king_pos[1]) <= 1:
                        return True
    return False
