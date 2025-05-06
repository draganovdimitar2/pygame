from chess.pieces.piece import Piece


class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        # One square in any direction
        self.directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # up, down, left, right
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # diagonals
        ]

    def current_possible_moves(self, board):
        possible_moves = []
        for dr, dc in self.directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target == '.' or target.color != self.color:
                    possible_moves.append((r, c))
        return possible_moves

    def __repr__(self):
        return f'{self.color}_king'
