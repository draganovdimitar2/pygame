from chess.pieces.piece import Piece


class Queen(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

    def current_possible_moves(self, board):
        possible_moves = []
        for dr, dc in self.directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target == '.':
                    possible_moves.append((r, c))
                else:
                    if target.color != self.color:
                        possible_moves.append((r, c))  # capture
                    break  # blocked
                r += dr
                c += dc
        return possible_moves

    def __repr__(self):
        return f'queen_{self.color}'
