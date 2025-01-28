import pygame
from sys import exit
from random import randint
from bird import Bird
from pipes import Pipes

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
FPS = 60
INITIAL_GAP = 150


def spawn_pipes(pipes, gap):
    down_pipe_y = randint(400, 630)
    lower_pipe = Pipes(is_upper=False, down_pipe_y=down_pipe_y)
    upper_pipe = Pipes(is_upper=True, down_pipe_y=down_pipe_y)
    pipes.add(lower_pipe, upper_pipe)


def reset_game(bird_group, pipes):
    """Reset the game state for a new round."""
    global points, game_active, gap
    pipes.empty()  # Clear the pipes
    spawn_pipes(pipes, gap)  # Spawn new pipes
    bird_group.empty()  # Clear the bird group
    bird_sprite = Bird()  # Create a new bird instance
    bird_group.add(bird_sprite)  # Add the bird to the group

    gap = 150
    points = 0.0  # Reset points to 0.0
    game_active = True  # Set the game state to active


def main():
    global game_active, gap, points  # Declare globals here for access in the main function
    pygame.init()  # always used to initialize the game
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # set the display dimensions
    clock = pygame.time.Clock()

    pygame.display.set_caption("Flappy Bird")  # name of the display
    points_font = pygame.font.SysFont(name='arial', size=75, bold=True)  # used for points counter

    game_active = True
    gap = INITIAL_GAP
    points = 0.0  # Points counter

    background_surface = pygame.image.load('graphics/background.png').convert()
    game_over_surface = pygame.image.load('graphics/game_over.png').convert_alpha()
    play_again_button = pygame.image.load("graphics/play_again_button.jpg").convert_alpha()
    play_again_button_rect = play_again_button.get_rect(center=(240, 540))

    bird_group = pygame.sprite.GroupSingle()  # single sprite group for the bird
    bird_sprite = Bird()
    bird_group.add(bird_sprite)

    pipes = pygame.sprite.Group()  # group for the pipes
    spawn_pipes(pipes, gap)
    while True:  # game loop
        for event in pygame.event.get():  # to get ell the events and loop through them
            if event.type == pygame.QUIT:  # to close the window
                pygame.quit()  # opposite to pygame.init()
                exit()  # to break the while loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_sprite.velocity_y = bird_sprite.flap_strength
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    bird_sprite.jump_sound.play()  # song for each bird jump

        if game_active:
            screen.blit(background_surface, (0, 0))
            pipes.update()
            pipes.draw(screen)

            # Spawn new pipes when the last pipe is off the screen
            if len(pipes) == 0 or pipes.sprites()[-1].rect.right < 0:  # Check if the last pipe is off the screen
                spawn_pipes(pipes, gap)

            bird_group.update()  # call the update method of out Bird class
            bird_group.draw(screen)  # add bird to the screen

            # Check if the bird has passed the last pipe
            for pipe in pipes:
                if pipe.rect.right < bird_group.sprite.rect.left and not pipe.passed:  # Check if bird passed the pipe
                    points += 0.5  # for each passed pipe increase score by 0.5 so when pass upper and lower pipe score += 1
                    pipe.passed = True  # Set flag to avoid multiple increments
                    bird_sprite.point_sound.play()
                    if gap > 120:  # min gap is 120
                        gap -= 0.5

            points_display = int(points)  # display the points as integer

            # Update points surface dynamically
            points_surface = points_font.render(str(points_display), False, 'Black')
            points_rect = points_surface.get_rect(center=(240, 50))  # Center for the score
            screen.blit(points_surface, points_rect)  # Draw points

            collision = pygame.sprite.spritecollide(
                bird_group.sprite,  # The single sprite from bird_group
                pipes,  # The group containing all pipe sprites
                False  # Keep the pipes in the group after collision (don't remove them)
            )

            if collision or bird_group.sprite.rect.top <= 0 or bird_group.sprite.rect.bottom >= screen.get_height():
                bird_sprite.die_sound.play()
                game_active = False  # End the game if collision occurs or bird is out of bounds
        else:
            game_over_rect = game_over_surface.get_rect(center=(240, 400))
            play_again_button_rect = play_again_button.get_rect(center=(240, 540))
            screen.blit(play_again_button, play_again_button_rect)
            screen.blit(game_over_surface, game_over_rect)
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_active:
                if play_again_button_rect.collidepoint(mouse_pos):
                    reset_game(bird_group, pipes)  # Call the reset function

        pygame.display.update()  # to update everything on our display surface
        clock.tick(FPS)  # to tell the while loop to not run faster than 60 fps


if __name__ == '__main__':
    main()
