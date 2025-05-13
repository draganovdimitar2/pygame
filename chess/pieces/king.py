from chess.pieces.piece import Piece


class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        # One square in any direction
        self.directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # up, down, left, right
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # diagonals
        ]
        self.has_moved = False

    def current_possible_moves(self, board):
        possible_moves = []
        for dr, dc in self.directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target == '.' or target.color != self.color:
                    possible_moves.append((r, c))
        return possible_moves

    def would_be_in_check(self, board, new_row, new_col):
        """
        Simulate moving the king to (new_row, new_col) and check if it's attacked.
        """
        original_row, original_col = self.row, self.col
        captured_piece = board[new_row][new_col]
        board[original_row][original_col] = '.'
        board[new_row][new_col] = self
        self.row, self.col = new_row, new_col

        # check if any opponent piece can attack this square
        for row in board:
            for piece in row:
                if piece != '.' and piece.color != self.color:
                    if (new_row, new_col) in piece.current_possible_moves(board):
                        # undo move
                        board[new_row][new_col] = captured_piece
                        board[original_row][original_col] = self
                        self.row, self.col = original_row, original_col
                        return True

        # undo move
        board[new_row][new_col] = captured_piece
        board[original_row][original_col] = self
        self.row, self.col = original_row, original_col
        return False

    def __repr__(self):
        return f'king_{self.color}'
