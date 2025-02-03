import pygame
from pygame.math import Vector2
from settings import CELL_NUMBER, CELL_SIZE
from random import randint

snake_rect_x = randint(0, 600)
snake_rect_y = randint(0, 600)


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  # to list to keep the body parts of the snake
        self.direction = Vector2(1, 0)  # moving to the right by default

    def draw_snake(self, screen):
        for block in self.body:
            # create and draw rect for each block of the snake
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_NUMBER)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        body_copy = self.body[:-1]  # taking each body part of the snake without it's head
        body_copy.insert(0, body_copy[0] + self.direction)  # insert the snake's head based on user input direction
        self.body = body_copy[:]  # return the entire list to the body

    def add_block(self):
        x_pos = self.body[-1].x + 1  # incrementing the x position of the last body part of the snake with 1
        y_pos = self.body[-1].y  # y remain the same
        self.body.append(Vector2(x_pos, y_pos))
