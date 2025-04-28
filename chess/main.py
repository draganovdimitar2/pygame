import pygame
from sys import exit
from settings import SCREEN_SIZE
from chess.board import Board

board_instance = Board()
board_without_pieces = board_instance.draw_board()
board_with_pieces = Board.draw_pieces_on_board(board_without_pieces)

running = True
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

turn_counter = 0  # if turn % 2 != 0 it is white pieces turn
while running:
    # draw_board()
    pygame.display.update()
    for event in pygame.event.get():  # to get ell the events and loop through them
        if event.type == pygame.QUIT:  # to close the window
            pygame.quit()  # opposite to pygame.init()
            running = False
            exit()

    clock.tick(60)
