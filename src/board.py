import pygame

from moves import is_king_in_check, is_valid_move

# --- Constantes ---
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CHECK_COLOR = (255, 0, 0)
HIGHLIGHT = (200, 200, 100)
POSSIBLE_MOVE_COLOR = (100, 200, 100)
SQUARE_SIZE = 600 // 8

def init_board():
    """Initialize the chess board and return the board data along with king positions."""
    board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    if not isinstance(board, list) or not all(isinstance(row, list) for row in board):
        raise ValueError("Invalid board structure in init_board")
    white_king_pos = (7, 4)  # Initial position of the white king
    black_king_pos = (0, 4)  # Initial position of the black king
    return board, white_king_pos, black_king_pos

def reset_board():
    """Reset the board to the initial position."""
    return init_board()

def get_king_position(board, white_turn):
    """Find the position of the king for the current player."""
    for r in range(8):
        for c in range(8):
            if board[r][c] == ('K' if white_turn else 'k'):
                return (r, c)
    return None

def get_possible_moves(board, selected_piece, white_turn, last_pawn_double_move, castling_rights):
    """Get all possible moves for the selected piece"""
    possible_moves = []
    
    # Check if a piece is selected
    if selected_piece is None:
        return []
        
    start_row, start_col = selected_piece
    piece = board[start_row][start_col]
    
    # Check all possible board positions
    for end_row in range(8):
        for end_col in range(8):
            if is_valid_move(board, start_row, start_col, end_row, end_col, white_turn, last_pawn_double_move, castling_rights):
                possible_moves.append((end_row, end_col))
                
                # Special case for castling - add intermediate squares for visualization
                if piece.lower() == 'k' and abs(end_col - start_col) == 2:
                    # For kingside castling, also highlight the square the rook will move to
                    if end_col > start_col:
                        possible_moves.append((start_row, 5))  # F1/F8 - where rook goes
                    # For queenside castling, also highlight the square the rook will move to
                    else:
                        possible_moves.append((start_row, 3))  # D1/D8 - where rook goes

    return possible_moves

def is_checkmate(board, white_turn, castling_rights, last_pawn_double_move, white_king_pos, black_king_pos):
    """Check if the current player is in checkmate."""
    if not isinstance(board, list) or not all(isinstance(row, list) for row in board):
        raise ValueError("Invalid board structure passed to is_checkmate")
    king_pos = white_king_pos if white_turn else black_king_pos
    if not is_king_in_check(board, white_turn, king_pos, castling_rights):
        return False

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != ' ' and ((piece.isupper() and white_turn) or (piece.islower() and not white_turn)):
                for nr in range(8):
                    for nc in range(8):
                        if is_valid_move(board, r, c, nr, nc, white_turn, last_pawn_double_move, castling_rights):
                            temp_board = [row[:] for row in board]
                            temp_board[nr][nc] = temp_board[r][c]
                            temp_board[r][c] = ' '
                            new_king_pos = (nr, nc) if (r, c) == king_pos else king_pos
                            if not is_king_in_check(temp_board, white_turn, new_king_pos, castling_rights):
                                return False

    # Additional check for knights causing checkmate
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece.lower() == 'n' and ((piece.islower() and not white_turn) or (piece.isupper() and white_turn)):
                if is_valid_move(board, r, c, king_pos[0], king_pos[1], not white_turn, last_pawn_double_move, castling_rights):
                    return True

    return True

def draw_checkmate_message(screen, white_turn):
    """Display a checkmate message on the board."""
    font = pygame.font.Font(None, 72)
    message = "White Wins!" if not white_turn else "Black Wins!"
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(600 // 2, 600 // 2))
    screen.blit(text, text_rect)

def draw_square(screen, row, col, color):
    """Draw a single square on the board."""
    pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_piece(screen, piece, pieces, row, col):
    """Draw a single piece on the board."""
    if piece != ' ':
        piece_img = pieces[piece]
        img_rect = piece_img.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
        screen.blit(piece_img, img_rect)

def draw_board(screen, board_data, selected_piece, pieces, white_turn, last_pawn_double_move, castling_rights):
    """Draw the entire chess board and its pieces."""
    board, white_king_pos, black_king_pos = board_data  # Unpack the board data correctly
    king_pos = get_king_position(board, white_turn) if is_king_in_check(board, white_turn, castling_rights=castling_rights) else None
    possible_moves = get_possible_moves(board, selected_piece, white_turn, last_pawn_double_move, castling_rights)

    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            if king_pos and king_pos == (row, col):
                color = CHECK_COLOR
            draw_square(screen, row, col, color)
            if selected_piece == (row, col):
                draw_square(screen, row, col, HIGHLIGHT)
            if (row, col) in possible_moves:
                pygame.draw.circle(screen, POSSIBLE_MOVE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 4)
            draw_piece(screen, board[row][col], pieces, row, col)

    if is_checkmate(board, white_turn, castling_rights, last_pawn_double_move, white_king_pos, black_king_pos):
        draw_checkmate_message(screen, white_turn)
