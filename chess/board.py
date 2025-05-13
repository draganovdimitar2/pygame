from chess.pieces.queen import Queen
from chess.pieces.rook import Rook
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn
from chess.pieces.king import King


class Board:
    def __init__(self):
        self.board = self.draw_board()
        self.draw_pieces_on_board()

    def draw_board(self):
        board = []
        for i in range(8):
            if i == 0:
                board.append(['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'])  # first row for white pieces
                continue
            elif i == 1:
                board.append(['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'])  # second row for white pieces
                continue
            elif i == 6:
                board.append(['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'])  # second row for black pieces
                continue
            elif i == 7:
                board.append(['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'])  # first row for black pieces
                continue
            board.append(['.'] * 8)  # Empty rows for other squares

        return board

    def create_piece(self, piece_code, row, col, color):
        piece_map = {
            'R': Rook,
            'N': Knight,
            'P': Pawn,
            'B': Bishop,
            'Q': Queen,
            'K': King
        }

        if piece_code == '.':
            return None

        piece_class = piece_map.get(piece_code)
        return piece_class(row, col, color)

    def draw_pieces_on_board(self):
        for row in range(8):
            for col in range(8):
                piece_code = self.board[row][col]
                if piece_code != '.':
                    color = 'b' if row < 2 else 'w'
                    self.board[row][col] = self.create_piece(piece_code, row, col, color)
