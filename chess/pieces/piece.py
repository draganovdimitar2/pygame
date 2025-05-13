from abc import ABC, abstractmethod
import pygame
from chess.visualisation import images
from chess.settings import SQUARE_SIZE


class Piece(ABC):  # abstract class for all pieces
    POSSIBLE_COLORS = ['b', 'w']

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.moves = {}  # dict to store the moves for each piece
        self.image = pygame.transform.scale(images[self.__repr__()], (SQUARE_SIZE, SQUARE_SIZE))

    @abstractmethod
    def current_possible_moves(self, board):
        pass
