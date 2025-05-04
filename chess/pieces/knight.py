from chess.pieces.piece import Piece


class Knight(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.possible_moves = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]

    def current_possible_moves(self, board):
        possible_moves = []
        for dr, dc in self.possible_moves:
            row = self.row + dr
            col = self.col + dc
            if 0 <= row < 8 and 0 <= col < 8:
                target = board[row][col]
                if target == '.' or target.color != self.color:
                    possible_moves.append((row, col))
        return possible_moves

    def __repr__(self):
        return f'{self.color}_knight'
