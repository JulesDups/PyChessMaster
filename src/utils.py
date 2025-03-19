import pygame

def load_images():
    pieces = {
        'k': pygame.image.load("../assets/img/king_black.png"),
        'K': pygame.image.load("../assets/img/king_white.png"),
        'q': pygame.image.load("../assets/img/queen_black.png"),
        'Q': pygame.image.load("../assets/img/queen_white.png"),
        'b': pygame.image.load("../assets/img/bishop_black.png"),
        'B': pygame.image.load("../assets/img/bishop_white.png"),
        'n': pygame.image.load("../assets/img/knight_black.png"),
        'N': pygame.image.load("../assets/img/knight_white.png"),
        'r': pygame.image.load("../assets/img/rook_black.png"),
        'R': pygame.image.load("../assets/img/rook_white.png"),
        'p': pygame.image.load("../assets/img/pawn_black.png"),
        'P': pygame.image.load("../assets/img/pawn_white.png"),
    }
    return pieces
