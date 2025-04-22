import pygame
from chess.settings import SQUARE_SIZE, X_UPPER_BOUNDARY, X_LOWER_BOUNDARY, Y_UPPER_BOUNDARY, Y_LOWER_BOUNDARY


class BlackPawn(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load('images/black_pieces/pawn_b.png').convert_alpha(),
            (SQUARE_SIZE, SQUARE_SIZE)
        )  # make the image 100x100 pixels
        self.rect = self.image.get_rect(topleft=(x, y))  # by default it is positioned on (0, 0)
        self.selected = False
        self.original_y = y  # to track first move (to know if the pawn can go 2 squares forward)

    def current_possible_moves(self):
        moves = []
        # One step forward
        one_step = (self.rect.x, self.rect.y + SQUARE_SIZE)
        if one_step[1] <= Y_UPPER_BOUNDARY:
            moves.append(one_step)
        # Two steps forward (only from starting row)
        if self.rect.y == self.original_y:
            two_steps = (self.rect.x, self.rect.y + 2 * SQUARE_SIZE)
            if two_steps[1] <= Y_UPPER_BOUNDARY:
                moves.append(two_steps)
        return moves

    def move(self, positions):
        self.rect.x = positions[0]
        self.rect.y = positions[1]
        self.selected = False
