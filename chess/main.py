import pygame
from chess.pieces.black.black_pawn import BlackPawn

SQUARE_SIZE = 100


def draw_board():
    colors = [pygame.Color((255, 204, 153)), pygame.Color("white")]
    for i in range(8):
        for j in range(8):
            color = colors[(i + j) % 2]
            pygame.draw.rect(screen, color,
                             pygame.Rect(i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


running = True
pygame.init()
screen = pygame.display.set_mode((800, 800))
black_pawn = BlackPawn(200, 200)
pawn_group = pygame.sprite.GroupSingle()
pawn_group.add(black_pawn)

while running:
    draw_board()
    pygame.display.update()
    pawn_group.draw(screen)

    for event in pygame.event.get():  # to get ell the events and loop through them
        if event.type == pygame.QUIT:  # to close the window
            pygame.quit()  # opposite to pygame.init()
            running = False
