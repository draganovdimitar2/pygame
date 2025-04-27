from chess.pieces.pawn import Pawn
from chess.pieces.knight import Knight
from chess.pieces.rook import Rook
from chess.pieces.bishop import Bishop
from chess.pieces.queen import Queen
from chess.pieces.king import King


class Board:
    @staticmethod
    def draw_board():
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
            board.append([])

            for j in range(8):
                board[i].append('.')

        return board

    @staticmethod
    def create_piece(piece_code, row, col, color):
        if piece_code == 'R':
            return Rook(row, col, color)
        elif piece_code == 'N':
            return Knight(row, col, color)
        elif piece_code == 'P':
            return Pawn(row, col, color)
        elif piece_code == 'B':
            return Bishop(row, col, color)
        elif piece_code == 'Q':
            return Queen(row, col, color)
        elif piece_code == 'K':
            return King(row, col, color)

    @staticmethod
    def draw_pieces_on_board(board):
        for row in range(8):
            for col in range(8):
                if row == 0 or row == 1:
                    board[row][col] = Board.create_piece(board[row][col], row, col, 'w')
                elif row == 6 or row == 7:
                    board[row][col] = Board.create_piece(board[row][col], row, col, 'b')
        return board
