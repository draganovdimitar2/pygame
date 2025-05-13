from chess.pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.forward = -1 if color == 'w' else 1
        self.reached_promotion_rank = False  # flag for promotion

    def current_possible_moves(self, board):
        moves = []
        r, c = self.row, self.col

        # forward one square
        if 0 <= r + self.forward < 8 and board[r + self.forward][c] == '.':
            moves.append((r + self.forward, c))

            if (self.color == 'w' and r == 6) or (self.color == 'b' and r == 1):
                if board[r + 2 * self.forward][c] == '.':
                    moves.append((r + 2 * self.forward, c))

        # diagonal left and right
        for dc in [-1, 1]:
            new_r, new_c = r + self.forward, c + dc
            if 0 <= new_r < 8 and 0 <= new_c < 8:
                target = board[new_r][new_c]
                if target != '.' and target.color != self.color:
                    moves.append((new_r, new_c))

        return moves

    def __repr__(self):
        return f'pawn_{self.color}'
