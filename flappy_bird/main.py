import pygame
from sys import exit
from random import randint


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # to inherit from the base class
        self.bird_jump = pygame.image.load('graphics/bird_jumping.png').convert_alpha()
        self.bird_falling = pygame.image.load('graphics/bird_falling.png').convert_alpha()
        self.bird_horizontal = pygame.image.load('graphics/bird.png').convert_alpha()

        self.image = self.bird_horizontal  # default bird position is horizontal
        self.rect = self.image.get_rect(topleft=(50, 200))
        self.velocity_y = 0  # velocity variable for smooth movement
        self.gravity = 0.5
        self.flap_strength = -6  # adjusted jump strength

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game_active:
            self.velocity_y = self.flap_strength  # set the velocity on jump

    def apply_gravity(self):
        self.velocity_y += self.gravity  # apply gravity to velocity
        self.rect.y += self.velocity_y  # update bird's position based on velocity

    def animation_state(self):
        # Update animation based on vertical position
        if self.velocity_y < 0:  # bird is going up
            self.image = self.bird_jump
        elif self.velocity_y >= 0:  # bird is falling or horizontal
            self.image = self.bird_falling

        # Ensure the image rect is updated based on the bird's position
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


down_pipe_y = randint(400, 630)  # random number for lower pipe y
gap = 150  # the gap between pipes
upper_pipe_y = down_pipe_y - gap


class Pipes(pygame.sprite.Sprite):
    def __init__(self, is_upper=False, down_pipe_y=None):
        super().__init__()
        self.image = pygame.image.load('graphics/pipe.png').convert_alpha()
        self.passed = False  # to track if the pipe has been passed by the bird
        if is_upper:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midbottom=(480, down_pipe_y - gap))  # Place upper pipe
        else:
            self.rect = self.image.get_rect(midtop=(480, down_pipe_y))  # Place lower pipe

    def update(self):
        # Move the pipe to the left
        self.rect.x -= 5
        # If the pipe moves off the screen, kill it (remove from group)
        if self.rect.right < 0:
            self.kill()


def spawn_pipes():
    down_pipe_y = randint(400, 630)
    lower_pipe = Pipes(is_upper=False, down_pipe_y=down_pipe_y)
    upper_pipe = Pipes(is_upper=True, down_pipe_y=down_pipe_y)
    pipes.add(lower_pipe, upper_pipe)


def reset_game():
    """Reset the game state for a new round."""
    global points, game_active, gap
    pipes.empty()  # Clear the pipes
    spawn_pipes()  # Spawn new pipes
    bird_group.empty()  # Clear the bird group
    bird_sprite = Bird()  # Create a new bird instance
    bird_group.add(bird_sprite)  # Add the bird to the group

    gap = 150
    points = 0.0  # Reset points to 0.0
    game_active = True  # Set the game state to active


pygame.init()  # always used to initialize the game
screen = pygame.display.set_mode((480, 800))  # set the display dimensions
clock = pygame.time.Clock()
FPS = 60

pygame.display.set_caption("Flappy Bird")  # name of the display
points_font = pygame.font.SysFont(name='arial', size=75, bold=True)  # used for points counter

game_active = True
points = 0.0  # points counter

background_surface = pygame.image.load('graphics/background.png').convert()
game_over_surface = pygame.image.load('graphics/game_over.png').convert_alpha()
play_again_button = pygame.image.load("graphics/play_again_button.jpg").convert_alpha()
play_again_button_rect = play_again_button.get_rect(center=(240, 540))

bird_group = pygame.sprite.GroupSingle()  # single sprite group for the bird
bird_sprite = Bird()
bird_group.add(bird_sprite)

pipes = pygame.sprite.Group()  # group for the pipes
spawn_pipes()

while True:  # our game runs withing this loop
    for event in pygame.event.get():  # to get ell the events and loop through them
        if event.type == pygame.QUIT:  # to close the window
            pygame.quit()  # opposite to pygame.init()
            exit()  # to break the while loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_sprite.velocity_y = bird_sprite.flap_strength

    if game_active:
        screen.blit(background_surface, (0, 0))
        pipes.update()
        pipes.draw(screen)

        # Spawn new pipes when the last pipe is off the screen
        if len(pipes) == 0 or pipes.sprites()[-1].rect.right < 0:  # Check if the last pipe is off the screen
            spawn_pipes()

        bird_group.update()  # call the update method of out Bird class
        bird_group.draw(screen)  # add bird to the screen

        # Check if the bird has passed the last pipe
        for pipe in pipes:
            if pipe.rect.right < bird_group.sprite.rect.left and not pipe.passed:  # Check if bird passed the pipe
                points += 0.5  # for each passed pipe increase score by 0.5 so when pass upper and lower pipe score += 1
                pipe.passed = True  # Set flag to avoid multiple increments
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
            game_active = False  # End the game if collision occurs or bird is out of bounds
    else:
        game_over_rect = game_over_surface.get_rect(center=(240, 400))
        play_again_button_rect = play_again_button.get_rect(center=(240, 540))
        screen.blit(play_again_button, play_again_button_rect)
        screen.blit(game_over_surface, game_over_rect)
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_active:
            if play_again_button_rect.collidepoint(mouse_pos):
                reset_game()  # Call the reset function

    pygame.display.update()  # to update everything on our display surface
    clock.tick(FPS)  # to tell the while loop to not run faster than 60 fps
