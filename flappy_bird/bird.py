import pygame


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

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.point_sound = pygame.mixer.Sound('audio/point.mp3')
        self.die_sound = pygame.mixer.Sound('audio/die.mp3')

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
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
