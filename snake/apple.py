import pygame, random
from pygame.math import Vector2
from settings import CELL_NUMBER, CELL_SIZE


class Apple:

    def __init__(self):
        self.randomize()

    def draw_apple(self, screen, apple):
        apple_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(apple, apple_rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)
