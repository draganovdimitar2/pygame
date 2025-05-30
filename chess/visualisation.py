import pygame
from chess.settings import SIDEBAR_WIDTH, SQUARE_SIZE

images = {
    'pawn_w': pygame.image.load('images/pawn_w.png'),
    'pawn_b': pygame.image.load('images/pawn_b.png'),
    'knight_w': pygame.image.load('images/knight_w.png'),
    'knight_b': pygame.image.load('images/knight_b.png'),
    'rook_w': pygame.image.load('images/rook_w.png'),
    'rook_b': pygame.image.load('images/rook_b.png'),
    'bishop_w': pygame.image.load('images/bishop_w.png'),
    'bishop_b': pygame.image.load('images/bishop_b.png'),
    'queen_w': pygame.image.load('images/queen_w.png'),
    'queen_b': pygame.image.load('images/queen_b.png'),
    'king_w': pygame.image.load('images/king_w.png'),
    'king_b': pygame.image.load('images/king_b.png')
}


def draw_board(screen, sq_size):
    """Draw the chessboard grid."""
    colors = [pygame.Color(255, 204, 153), pygame.Color(255, 255, 255)]  # dark and light squares
    for i in range(8):
        for j in range(8):
            color = colors[(i + j) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(i * sq_size, j * sq_size, sq_size, sq_size))


def draw_pieces(board, screen, sq_size):
    """Draw the pieces on the board."""
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '.':
                # 1. determine piece type and color (e.g., 'rook_w' or 'rook_b')
                piece_type = f"{piece.__repr__()}"

                # 2. scale image to fit the square size
                piece_image = pygame.transform.scale(images[piece_type], (sq_size, sq_size))

                # 3. draw the piece on the board
                screen.blit(piece_image, (col * sq_size, row * sq_size))


def draw_sidebar(win, game_state, captured_white, captured_black):
    """
    Draw the right-hand sidebar showing game info and captured pieces.
    """
    font = pygame.font.SysFont('Arial', 24)
    small_font = pygame.font.SysFont('Arial', 20)

    # background
    sidebar_rect = pygame.Rect(SQUARE_SIZE * 8, 0, SIDEBAR_WIDTH, SQUARE_SIZE * 8)
    pygame.draw.rect(win, (230, 230, 230), sidebar_rect)

    # turn display
    turn_text = font.render(f"Turn: {'White' if game_state.turn() == 'w' else 'Black'}", True, (0, 0, 0))
    win.blit(turn_text, (SQUARE_SIZE * 8 + 5, 20))

    # captured pieces
    win.blit(small_font.render("White captures:", True, (0, 0, 0)), (SQUARE_SIZE * 8 + 5, 80))
    for i, piece in enumerate(captured_white):
        scaled_piece = pygame.transform.scale(piece.image, (SQUARE_SIZE // 2, SQUARE_SIZE // 2))
        win.blit(scaled_piece, (SQUARE_SIZE * 8 + 5 + (i % 3) * 50, 110 + (i // 3) * 50))

    win.blit(small_font.render("Black captures:", True, (0, 0, 0)), (SQUARE_SIZE * 8 + 5, 450))
    for i, piece in enumerate(captured_black):
        scaled_piece = pygame.transform.scale(piece.image, (SQUARE_SIZE // 2, SQUARE_SIZE // 2))
        win.blit(scaled_piece, (SQUARE_SIZE * 8 + 5 + (i % 3) * 50, 480 + (i // 3) * 50))


def draw_game_over(win, game_state):
    """
    Display the game over screen with the winner's name.
    """
    # increase font sizes for a more dramatic effect
    font_big = pygame.font.SysFont('Arial', 120, bold=True)  # larger font for "Game Over"
    font_medium = pygame.font.SysFont('Arial', 80)  # larger font for winner's name
    font_small = pygame.font.SysFont('Arial', 50)  # font for game reset

    # create text objects
    game_over_text = font_big.render('Game Over!', True, (0, 0, 0))
    winner = 'Black' if game_state.b_wins else 'White'
    who_won_text = font_medium.render(f'{winner} wins', True, (0, 0, 0))
    reset_option = font_small.render("Press Left Mouse Button to reset the game.", True, (0, 0, 0))

    # center the texts on the screen
    game_over_rect = game_over_text.get_rect(center=(win.get_width() // 2, win.get_height() // 2 - 80))
    who_won_rect = who_won_text.get_rect(center=(win.get_width() // 2, win.get_height() // 2 + 40))
    reset_rect = reset_option.get_rect(center=(win.get_width() // 2, win.get_height() // 2 + 110))
    # draw the texts on the screen
    win.blit(game_over_text, game_over_rect)
    win.blit(who_won_text, who_won_rect)
    win.blit(reset_option, reset_rect)


def draw_promotion_menu(screen, color):
    """
    Display the promotion menu for pawn promotion.
    """
    menu_width = 4 * SQUARE_SIZE
    menu_height = SQUARE_SIZE
    x = (screen.get_width() - menu_width) // 2
    y = (screen.get_height() - menu_height) // 2

    pygame.draw.rect(screen, (60, 60, 60), (x, y, menu_width, menu_height))

    pieces = ['queen', 'rook', 'bishop', 'knight']
    scaled_images = []  # list to store image rects and piece names

    for i, piece_name in enumerate(pieces):
        image_key = f'{piece_name}_{color}'
        piece_image = images[image_key]
        piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))  # scale the image
        image_rect = piece_image.get_rect(center=(x + i * SQUARE_SIZE + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
        scaled_images.append((piece_image, image_rect, piece_name))  # store the image, rect, and piece name

        screen.blit(piece_image, image_rect)  # draw the image on the screen

    return scaled_images  # return the list of scaled images and their rects


def highlight_king_in_check(screen, king_pos, square_size):
    """Draw a red square around the king if in check."""
    row, col = king_pos
    red = (255, 0, 0)
    rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
    pygame.draw.rect(screen, red, rect, 5)  # 5 is the border width
