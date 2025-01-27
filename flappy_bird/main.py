import pygame
from sys import exit
from random import randint

pygame.init()  # always used to initialize the game
screen = pygame.display.set_mode((480, 800))  # set the display dimensions
clock = pygame.time.Clock()
fps = 60

pygame.display.set_caption("Flappy Bird")  # name of the display
points_font = pygame.font.SysFont(name='arial', size=75, bold=True)  # used for points counter

game_active = True
player_gravity = 0
gap = 160  # each 5 points increase, the gap will decrease with 5 px
points = 0
pipe_passed = False  # flag to check whether bird has passed the pipe

background_surface = pygame.image.load('graphics/background.png').convert()
game_over_surface = pygame.image.load('graphics/game_over.png').convert_alpha()
play_again_button = pygame.image.load("graphics/play_again_button.jpg").convert_alpha()
down_pipe_sur = pygame.image.load('graphics/pipe.png').convert_alpha()
pipe_width = down_pipe_sur.get_width()
pipe_height = down_pipe_sur.get_height()

upper_pipe_sur = pygame.transform.flip(down_pipe_sur, False, True)
bird_surface = pygame.image.load('graphics/bird.png').convert_alpha()
bird_rect = bird_surface.get_rect(topleft=(50, 200))


def generate_pipes():
    down_pipe_y = randint(400, 630)
    down_pipe_rect = down_pipe_sur.get_rect(midtop=(480, down_pipe_y))
    upper_pipe_y = down_pipe_y - gap
    upper_pipe_rect = upper_pipe_sur.get_rect(midbottom=(480, upper_pipe_y))
    return down_pipe_rect, upper_pipe_rect


down_pipe_rect, upper_pipe_rect = generate_pipes()
print(f'down: {down_pipe_rect.y}')
while True:  # our game runs withing this loop
    for event in pygame.event.get():  # to get ell the events and loop through them
        if event.type == pygame.QUIT:  # to close the window
            pygame.quit()  # opposite to pygame.init()
            exit()  # to break the while loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                player_gravity = -11

    if game_active:
        screen.blit(background_surface, (0, 0))

        down_pipe_rect.x -= 5  # to move the pipes left
        upper_pipe_rect.x -= 5  # to move the pipes left
        screen.blit(down_pipe_sur, down_pipe_rect)  # add pipes to the screen
        screen.blit(upper_pipe_sur, upper_pipe_rect)

        if down_pipe_rect.right < 0:
            down_pipe_rect, upper_pipe_rect = generate_pipes()
            pipe_passed = False  # reset the flag

        player_gravity += 1  # add gravity to update bird position
        bird_rect.y += player_gravity
        screen.blit(bird_surface, bird_rect)  # add bird to the screen

        # Check if bird passed the pipe
        if not pipe_passed and bird_rect.x > down_pipe_rect.x + pipe_width:
            points += 1  # Increment points
            if points % 5 == 0 and gap > 125:
                gap -= 5
            pipe_passed = True  # Set flag to avoid multiple increments

        # Update points surface dynamically
        points_surface = points_font.render(str(points), False, 'Black')
        points_rect = points_surface.get_rect(center=(240, 50))  # Center for the score
        screen.blit(points_surface, points_rect)  # Draw points

        if down_pipe_rect.x == 0:
            down_pipe_rect.x = 480
            upper_pipe_rect.x = 480

            # Check for collisions
        if (bird_rect.colliderect(down_pipe_rect) or
                bird_rect.colliderect(upper_pipe_rect) or
                bird_rect.top < 0 or bird_rect.bottom >= screen.get_height()):  # Prevent bird from going off-screen
            game_active = False
    else:
        game_over_rect = game_over_surface.get_rect(center=(240, 400))
        play_again_button_rect = play_again_button.get_rect(center=(240, 540))
        screen.blit(play_again_button, play_again_button_rect)
        screen.blit(game_over_surface, game_over_rect)
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_active:
            if play_again_button_rect.collidepoint(pygame.mouse.get_pos()):
                # Reset game state
                bird_rect.topleft = (50, 200)
                player_gravity = 0
                down_pipe_rect, upper_pipe_rect = generate_pipes()
                points = 0
                pipe_passed = False
                game_active = True

    pygame.display.update()  # to update everything on our display surface
    clock.tick(fps)  # to tell the while loop to not run faster than 60 fps
