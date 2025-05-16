import pygame
from settings import SQUARE_SIZE, SCREEN_SIZE
from chess.sound.sound_manager import SoundManager
from chess.game_state import GameState
from chess.visualisation import (
    draw_board, draw_pieces, draw_sidebar,
    draw_game_over, draw_promotion_menu,
    highlight_king_in_check
)


class GameController:
    """
    Handles the game loop rendering and input delegation.

    Manages the visual updates of the board, pieces, highlights,
    game-over states, and delegates input handling to the GameState.
    """

    def __init__(self, screen, sound_manager, game_state):
        self.sound_manager = sound_manager
        self.screen = screen
        self.game_state = game_state
        self.board = self.game_state.board_obj.board
        self.game_over = False
        self.scaled_images = []

    def update(self):
        self.screen.fill(pygame.Color(255, 255, 255))
        draw_board(self.screen, SQUARE_SIZE)

        if self.game_state.w_check:
            highlight_king_in_check(self.screen, self.game_state.w_king_pos, SQUARE_SIZE)
        if self.game_state.b_check:
            highlight_king_in_check(self.screen, self.game_state.b_king_pos, SQUARE_SIZE)

        draw_pieces(self.board, self.screen, SQUARE_SIZE)
        self.game_state.draw_highlighted_moves(self.screen, SQUARE_SIZE)
        draw_sidebar(self.screen, self.game_state, self.game_state.captured_white, self.game_state.captured_black)

        if self.game_state.promoting:
            self.scaled_images = draw_promotion_menu(self.screen, self.game_state.promotion_color)

        if self.game_state.b_wins or self.game_state.w_wins:
            draw_game_over(self.screen, self.game_state)
            self.game_over = True

        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and not self.game_over:
            pos = event.pos  # or pygame.mouse.get_pos()
            self.game_state.handle_click(pos[0], pos[1], self.board)

            if self.game_state.promoting:
                selected_piece = self.game_state.handle_promotion_click(
                    pos, self.scaled_images, self.game_state.promotion_color
                )
                if selected_piece:
                    self.game_state.promote_pawn(selected_piece)
                    self.game_state.turn_counter += 1

        elif event.type == pygame.MOUSEBUTTONUP and self.game_over:  # handle game reset logic
            screen = pygame.display.set_mode(SCREEN_SIZE)
            sound = SoundManager()
            game_state = GameState(sound_manager=sound)
            new_controller = GameController(screen, sound, game_state)
            return new_controller
