import pygame
from random import randint

apple_rect_x = randint(0, 600)
apple_rect_y = randint(0, 600)


class Apple(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/apple.png')
        self.rect = self.image.get_rect(midbottom = (apple_rect_x, apple_rect_y))
