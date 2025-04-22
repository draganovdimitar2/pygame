import pygame
from sys import exit
from chess.pieces.black.black_pawn import BlackPawn
from settings import SQUARE_SIZE, SCREEN_SIZE


def draw_board():
    colors = [pygame.Color((255, 204, 153)), pygame.Color("white")]
    for i in range(8):
        for j in range(8):
            color = colors[(i + j) % 2]
            pygame.draw.rect(screen, color,
                             pygame.Rect(i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


running = True
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

black_pieces_group = pygame.sprite.Group()  # the group for black pieces
for i in range(8):  # spawn all 8 pawns
    black_pawn = BlackPawn((SQUARE_SIZE * i), SQUARE_SIZE)
    black_pieces_group.add(black_pawn)

while running:
    draw_board()

    black_pieces_group.draw(screen)
    pygame.display.update()

    for event in pygame.event.get():  # to get ell the events and loop through them
        if event.type == pygame.QUIT:  # to close the window
            pygame.quit()  # opposite to pygame.init()
            running = False
            exit()

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for piece in black_pieces_group:
                # Only one pawn should be selected at a time
                if not piece.rect.collidepoint(mouse_pos) and piece.selected:  # if the piece is already selected move it
                    current_possible_moves = piece.current_possible_moves()  # fetch all possible moves
                    print(current_possible_moves)
                    for move in current_possible_moves:
                        move_rect = pygame.Rect(move[0], move[1], SQUARE_SIZE, SQUARE_SIZE)
                        if move_rect.collidepoint(mouse_pos):
                            piece.move(move)
                            print(piece.selected)
                elif piece.rect.collidepoint(mouse_pos) and not piece.selected:  # first select the piece
                    piece.selected = True
                    if piece.selected:
                        print(f"x = {piece.rect.x}, y = {piece.rect.y}")
                        print(mouse_pos)
                        print(piece.selected)


    clock.tick(60)
