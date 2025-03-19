import pygame
from utils import load_images
from board import init_board, draw_board, reset_board
from events import handle_events

# --- Constantes ---
WIDTH, HEIGHT = 600, 600

def initialize_game():
    """Initialize the game and return the necessary objects."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Échecs")
    pieces = load_images()
    board, white_king_pos, black_king_pos = init_board()  # Unpack king positions
    # Debugging: Print the structure of board_data
    print("Debug: board_data initialized:", board)
    return screen, pieces, board, white_king_pos, black_king_pos

def reset_game_state():
    """Reset the game state to the initial position."""
    board, white_king_pos, black_king_pos = reset_board()  # Unpack king positions
    # Debugging: Print the structure of board_data
    print("Debug: board_data reset:", board)
    selected_piece = None
    white_turn = True
    last_pawn_double_move = None
    # Use the simplified castling rights structure - we don't need the extra tracking flags
    castling_rights = {
        'white': {'kingside': True, 'queenside': True},
        'black': {'kingside': True, 'queenside': True}
    }
    return board, white_king_pos, black_king_pos, selected_piece, white_turn, last_pawn_double_move, castling_rights

# Remove or comment out the conflicting function
# def init_castling_rights():
#     """Initialize the castling rights for both players."""
#     return {
#         'white': {'kingside': True, 'queenside': True},
#         'white_king_moved': False,
#         'white_kingside_rook_moved': False,
#         'white_queenside_rook_moved': False,
#         'black': {'kingside': True, 'queenside': True},
#         'black_king_moved': False,
#         'black_kingside_rook_moved': False,
#         'black_queenside_rook_moved': False
#     }

def game_loop(screen, pieces, board, white_king_pos, black_king_pos):
    """Main game loop."""
    board, white_king_pos, black_king_pos, selected_piece, white_turn, last_pawn_double_move, castling_rights = reset_game_state()
    running = True

    while running:
        # Validate board structure before passing it to handle_events
        if not isinstance(board, list) or not all(isinstance(row, list) for row in board):
            # Debug: Print the actual structure of board
            print("Debug: board structure:", type(board), "contains:", board)
            raise ValueError("Invalid board structure in game_loop")
        
        # Create board_data tuple for draw_board function
        board_data = (board, white_king_pos, black_king_pos)
        
        selected_piece, white_turn, running, last_pawn_double_move, castling_rights, white_king_pos, black_king_pos = handle_events(
            board, selected_piece, white_turn, last_pawn_double_move, castling_rights, screen, pieces, white_king_pos, black_king_pos
        )
        
        if running:
            # Update board_data with current values
            board_data = (board, white_king_pos, black_king_pos)
            draw_board(screen, board_data, selected_piece, pieces, white_turn, last_pawn_double_move, castling_rights)
            pygame.display.flip()
        else:
            board_data = (board, white_king_pos, black_king_pos)
            draw_board(screen, board_data, selected_piece, pieces, white_turn, last_pawn_double_move, castling_rights)
            pygame.display.flip()  # Ensure the checkmate message is displayed before quitting

def main():
    """Main entry point of the program."""
    screen, pieces, board, white_king_pos, black_king_pos = initialize_game()
    game_loop(screen, pieces, board, white_king_pos, black_king_pos)
    pygame.quit()

if __name__ == "__main__":
    main()