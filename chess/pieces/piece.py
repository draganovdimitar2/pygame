from abc import ABC

class Piece(ABC):  # abstract class for all pieces
    POSSIBLE_COLORS = ['b', 'w']

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.moves = {}  # dict to store the moves for each piece

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        if value not in self.POSSIBLE_COLORS:
            return 'Possible colors are b and w'
        self.__color = value

    def current_possible_moves(self, board):
        pass
