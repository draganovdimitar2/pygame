import pygame

gap = 150


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
