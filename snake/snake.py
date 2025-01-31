import pygame
from random import randint

snake_rect_x = randint(0, 600)
snake_rect_y = randint(0, 600)


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/snake.png')
        self.rect = self.image.get_rect(midbottom=(snake_rect_x, snake_rect_y))

    def snake_moves(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y += 2
        if keys[pygame.K_DOWN]:
            self.rect.y += 2
        if keys[pygame.K_LEFT]:
            self.rect.x += 2
        if keys[pygame.K_RIGHT]:
            self.rect.x += 2

    def destroy(self):
        if self.rect.y >= 600 or self.rect.x >= 600:
            self.kill()

    def update(self):
        self.snake_moves()
        self.destroy()
