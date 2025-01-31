import pygame
from sys import exit
from snake import Snake
from apple import Apple


def collision_checker():
    return pygame.sprite.spritecollide(snake.sprite, apple, False)


WIDTH = 600
HEIGHT = 600
snake_movement = 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
game = pygame.init()
snake = pygame.sprite.GroupSingle()
snake.add(Snake())
apple = pygame.sprite.Group()
apple.add(Apple())
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    background_surface = pygame.Surface.fill(screen, 'White')
    apple.draw(screen)
    apple.update()
    snake.draw(screen)
    snake.update()

    if collision_checker():
        pass
    pygame.display.update()
    clock.tick(60)
