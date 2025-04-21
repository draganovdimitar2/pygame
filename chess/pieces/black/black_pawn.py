import pygame


class BlackPawn(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load('images/black_pieces/pawn_b.png')
        self.rect = self.image.get_rect()
        self.selected = False

    def player_input(self, screen, square_size):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.selected = True
            selected_color = (204, 255, 204)

            pygame.draw.rect(screen, selected_color,
                             pygame.Rect(self.x - square_size, self.y + square_size, square_size, square_size))
