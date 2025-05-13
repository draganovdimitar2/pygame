import pygame
from sys import exit
from settings import SCREEN_SIZE, SQUARE_SIZE
from chess.visualisation import draw_board, draw_pieces, draw_sidebar, draw_game_over, draw_promotion_menu, highlight_king_in_check
from chess.game_state import GameState

game_state = GameState()
# board instance
board_instance = game_state.board_obj


running = True
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
game_over = False
scaled_images = []

while running:
    screen.fill(pygame.Color(255, 255, 255))

    if not game_over:
        screen.fill(pygame.Color(255, 255, 255))

    draw_board(screen, SQUARE_SIZE)  # board visualisation
    if game_state.w_check:  # to make the king square in red if it is in check
        highlight_king_in_check(screen, game_state.w_king_pos, SQUARE_SIZE)
    if game_state.b_check:
        highlight_king_in_check(screen, game_state.b_king_pos, SQUARE_SIZE)
    draw_pieces(board_instance.board, screen, SQUARE_SIZE)   # pieces visualisation
    if game_state.promoting:
        # Draw the promotion menu if it's the player's turn to promote a pawn
        scaled_images = draw_promotion_menu(screen, game_state.promotion_color)

    game_state.draw_highlighted_moves(screen, SQUARE_SIZE)
    draw_sidebar(screen, game_state, game_state.captured_white, game_state.captured_black)
    # if the game is over
    if game_state.b_wins or game_state.w_wins:
        draw_game_over(screen, game_state)
        game_over = True  # set the game over flag to True to stop further processing

    pygame.display.update()

    for event in pygame.event.get():  # to get ell the events and loop through them
        if event.type == pygame.QUIT:  # to close the window
            pygame.quit()  # opposite to pygame.init()
            running = False
            exit()

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            game_state.handle_click(pos[0], pos[1], game_state.board_obj.board)

            if game_state.promoting and event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                selected_piece = game_state.handle_promotion_click(pos, scaled_images, game_state.promotion_color)
                if selected_piece:
                    game_state.promote_pawn(selected_piece)
                    game_state.turn_counter += 1  # increment the turn counter




clock.tick(60)
