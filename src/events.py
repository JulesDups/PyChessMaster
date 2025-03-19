import pygame
from moves import is_valid_move, is_king_in_check
from board import is_checkmate

def handle_events(board, selected_piece, white_turn, last_pawn_double_move, castling_rights, screen, pieces, white_king_pos, black_king_pos):
    # Validate board structure
    if not isinstance(board, list) or not all(isinstance(row, list) for row in board):
        raise ValueError("Invalid board structure passed to handle_events")
    if is_checkmate(board, white_turn, castling_rights, last_pawn_double_move, white_king_pos, black_king_pos):
        return selected_piece, white_turn, False, last_pawn_double_move, castling_rights, white_king_pos, black_king_pos  # Stop the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return handle_quit_event(last_pawn_double_move, castling_rights, white_king_pos, black_king_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            return handle_mouse_down_event(event, board, white_turn, selected_piece, last_pawn_double_move, castling_rights, white_king_pos, black_king_pos)
        if event.type == pygame.MOUSEBUTTONUP and selected_piece:
            return handle_mouse_up_event(event, board, selected_piece, white_turn, last_pawn_double_move, castling_rights, screen, pieces, white_king_pos, black_king_pos)
    return selected_piece, white_turn, True, last_pawn_double_move, castling_rights, white_king_pos, black_king_pos

def handle_quit_event(last_pawn_double_move, castling_rights, white_king_pos, black_king_pos):
    return None, None, False, last_pawn_double_move, castling_rights, white_king_pos, black_king_pos

def handle_mouse_down_event(event, board, white_turn, selected_piece, last_pawn_double_move, castling_rights, white_king_pos, black_king_pos):
    x, y = pygame.mouse.get_pos()
    row, col = y // (600 // 8), x // (600 // 8)
    piece = board[row][col]
    if piece != ' ' and ((piece.isupper() and white_turn) or (piece.islower() and not white_turn)):
        return (row, col), white_turn, True, last_pawn_double_move, castling_rights, white_king_pos, black_king_pos
    return selected_piece, white_turn, True, last_pawn_double_move, castling_rights, white_king_pos, black_king_pos

def handle_mouse_up_event(event, board, selected_piece, white_turn, last_pawn_double_move, castling_rights, screen, pieces, white_king_pos, black_king_pos):
    x, y = pygame.mouse.get_pos()
    new_row, new_col = y // (600 // 8), x // (600 // 8)
    if is_valid_move(board, selected_piece[0], selected_piece[1], new_row, new_col, white_turn, last_pawn_double_move, castling_rights):
        print(castling_rights)
        return process_valid_move(board, selected_piece, new_row, new_col, white_turn, last_pawn_double_move, castling_rights, screen, pieces, white_king_pos, black_king_pos)
    return selected_piece, white_turn, True, last_pawn_double_move, castling_rights, white_king_pos, black_king_pos

def process_valid_move(board, selected_piece, new_row, new_col, white_turn, last_pawn_double_move, castling_rights, screen, pieces, white_king_pos, black_king_pos):
    temp_board = [row[:] for row in board]
    temp_board[new_row][new_col] = temp_board[selected_piece[0]][selected_piece[1]]
    temp_board[selected_piece[0]][selected_piece[1]] = ' '
    if not is_king_in_check(temp_board, white_turn):
        update_board_for_move(board, selected_piece, new_row, new_col)
        
        # Update king positions if king is moved
        if board[new_row][new_col].lower() == 'k':
            if white_turn:
                white_king_pos = (new_row, new_col)
            else:
                black_king_pos = (new_row, new_col)
        
        # Create new references for the values that will be modified
        updated_pawn_move = last_pawn_double_move
        
        # Handle special moves - this modifies castling_rights and updated_pawn_move
        handle_special_moves(board, selected_piece, new_row, new_col, white_turn, updated_pawn_move, castling_rights, screen, pieces)
        
        # Update pawn double move correctly
        if board[new_row][new_col].lower() == 'p' and abs(new_row - selected_piece[0]) == 2:
            updated_pawn_move = (new_row, new_col)
        else:
            updated_pawn_move = None
            
        # Return updated values
        return None, not white_turn, True, updated_pawn_move, castling_rights, white_king_pos, black_king_pos
    
    return selected_piece, white_turn, True, last_pawn_double_move, castling_rights, white_king_pos, black_king_pos

def update_board_for_move(board, selected_piece, new_row, new_col):
    board[new_row][new_col] = board[selected_piece[0]][selected_piece[1]]
    board[selected_piece[0]][selected_piece[1]] = ' '

def handle_special_moves(board, selected_piece, new_row, new_col, white_turn, last_pawn_double_move, castling_rights, screen, pieces):
    handle_castling(board, selected_piece, new_row, new_col, white_turn, castling_rights)
    handle_pawn_promotion(board, new_row, new_col, white_turn, screen, pieces)
    handle_en_passant(board, selected_piece, new_row, new_col, last_pawn_double_move)
    update_castling_rights(board, selected_piece, new_row, new_col, white_turn, castling_rights)
    update_pawn_double_move(board, selected_piece, new_row, new_col, last_pawn_double_move)

def handle_castling(board, selected_piece, new_row, new_col, white_turn, castling_rights):
    if board[new_row][new_col].lower() == 'k' and abs(new_col - selected_piece[1]) == 2:
        # Debug print to verify castling is being triggered
        print(f"Castling from {selected_piece} to {new_row},{new_col}")
        
        if new_col > selected_piece[1]:  # Kingside castling
            print("Moving kingside rook from", (new_row, 7), "to", (new_row, 5))
            board[new_row][5] = board[new_row][7]  # Move rook to F1/F8
            board[new_row][7] = ' '  # Clear rook's original position
        else:  # Queenside castling
            print("Moving queenside rook from", (new_row, 0), "to", (new_row, 3))
            board[new_row][3] = board[new_row][0]  # Move rook to D1/D8
            board[new_row][0] = ' '  # Clear rook's original position
        
        # Update castling rights
        side = 'white' if white_turn else 'black'
        if side in castling_rights:
            castling_rights[side]['kingside'] = False
            castling_rights[side]['queenside'] = False

def handle_pawn_promotion(board, new_row, new_col, white_turn, screen, pieces):
    if board[new_row][new_col].lower() == 'p' and (new_row == 0 or new_row == 7):
        promoted_piece = get_promotion_choice_on_board(screen, pieces, white_turn)
        board[new_row][new_col] = promoted_piece

def handle_en_passant(board, selected_piece, new_row, new_col, last_pawn_double_move):
    if board[new_row][new_col].lower() == 'p' and last_pawn_double_move == (selected_piece[0], new_col):
        board[last_pawn_double_move[0]][last_pawn_double_move[1]] = ' '

def update_castling_rights(board, selected_piece, new_row, new_col, white_turn, castling_rights):
    # If the king moves, disable all castling for that side
    piece = board[new_row][new_col]
    side = 'white' if white_turn else 'black'
    
    if piece.lower() == 'k':
        if side in castling_rights:
            castling_rights[side]['kingside'] = False
            castling_rights[side]['queenside'] = False
    
    # If a rook moves, disable only that side's castling
    elif piece.lower() == 'r':
        if side in castling_rights:
            if selected_piece[1] == 0:  # Queenside rook
                castling_rights[side]['queenside'] = False
            elif selected_piece[1] == 7:  # Kingside rook
                castling_rights[side]['kingside'] = False

def update_pawn_double_move(board, selected_piece, new_row, new_col, last_pawn_double_move):
    # This function should modify the last_pawn_double_move object, not return a value
    # Since we're updating the last_pawn_double_move directly in process_valid_move, this function is unused
    pass

def get_promotion_choice(white_turn):
    # Display a simple menu for the user to choose the promotion piece
    options = ['q', 'r', 'b', 'n']  # Queen, Rook, Bishop, Knight
    while True:
        print("Choose a piece for promotion:")
        for i, option in enumerate(options):
            print(f"{i + 1}: {option.upper() if white_turn else option.lower()}")
        choice = input("Enter the number of your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= 4:
            return options[int(choice) - 1].upper() if white_turn else options[int(choice) - 1].lower()

def get_promotion_choice_gui(white_turn):
    # Use a graphical interface to choose the promotion piece
    pygame.init()
    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Choose Promotion Piece")
    font = pygame.font.Font(None, 36)
    options = ['Queen', 'Rook', 'Bishop', 'Knight']
    colors = [(255, 255, 255), (200, 200, 200)]
    selected = None

    while selected is None:
        screen.fill((0, 0, 0))
        for i, option in enumerate(options):
            color = colors[i % 2]
            text = font.render(option, True, color)
            rect = text.get_rect(center=(200, 50 * (i + 1)))
            screen.blit(text, rect)
            pygame.draw.rect(screen, color, rect, 2)
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if rect.collidepoint(mouse_pos):
                    selected = option.lower()[0]  # Return the first letter of the piece name
                    break
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    pygame.quit()
    return selected.upper() if white_turn else selected.lower()

def get_promotion_choice_on_board(screen, pieces, white_turn):
    # Display promotion options on the board
    options = ['q', 'r', 'b', 'n']  # Queen, Rook, Bishop, Knight
    piece_images = {  # Map piece letters to images
        'q': pieces['Q' if white_turn else 'q'],
        'r': pieces['R' if white_turn else 'r'],
        'b': pieces['B' if white_turn else 'b'],
        'n': pieces['N' if white_turn else 'n']
    }
    rects = []
    background_color = (50, 50, 50)  # Dark gray background for better visibility

    # Determine the position of the promotion square
    promotion_row = 0 if white_turn else 7
    promotion_y = promotion_row * (600 // 8)
    display_y = promotion_y + (600 // 8)  # Position below the promotion square

    # Draw background rectangle
    pygame.draw.rect(screen, background_color, (0, display_y, 600, 100))

    for i, option in enumerate(options):
        img = piece_images[option]
        rect = img.get_rect(center=(150 + i * 100, display_y + 50))  # Center images in the background area
        rects.append((rect, option))
        screen.blit(img, rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for rect, option in rects:
                    if rect.collidepoint(x, y):
                        return option.upper() if white_turn else option.lower()
