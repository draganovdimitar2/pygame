import pygame
from pygame.math import Vector2
from sys import exit
from apple import Apple
from snake import Snake
from settings import CELL_SIZE, CELL_NUMBER, FPS, MILLISECONDS


class MAIN:
    def __init__(self):
        self.snake = Snake()
        self.apple = Apple()

    def update(self):
        self.snake.move_snake()
        self.check_collision()

    def draw_elements(self):
        self.apple.draw_apple(screen)
        self.snake.draw_snake(screen)
        self.check_fail()

    def check_collision(self):
        if self.apple.pos == self.snake.body[0]:  # check if apple and head of the snake are at the same position
            self.apple.randomize()
            self.snake.add_block()

    def check_fail(self):  # checks if snake hits itself or going out of the screen
        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[
            0].y < CELL_NUMBER:  # check if snake is within the screen
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        exit()


pygame.init()
screen = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT  # we will use it in the event loop to generate the independent movement of the snake
pygame.time.set_timer(SCREEN_UPDATE, MILLISECONDS)  # timer that generates SCREEN_UPDATE every 150 milliseconds

main_game = MAIN()

while True:
    for event in pygame.event.get():  # event loop
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:  # nested if-statements prevent snake from reversing
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(FPS)
