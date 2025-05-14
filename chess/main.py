import pygame
from sys import exit
from settings import SCREEN_SIZE
from chess.game_state import GameState
from chess.sound.sound_manager import SoundManager
from chess.game_controller import GameController
from chess.settings import FPS

sound = SoundManager()
game_state = GameState(sound_manager=sound)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
controller = GameController(screen, sound, game_state)
clock = pygame.time.Clock()

game_over = False
running = True
while running:
    controller.update()

    for event in pygame.event.get():  # event loop
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            exit()

        controller.handle_event(event)

    clock.tick(FPS)
