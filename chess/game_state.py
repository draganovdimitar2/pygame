from chess.pieces.queen import Queen
from chess.pieces.rook import Rook
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn
from chess.board import Board
from chess.settings import SQUARE_SIZE
import pygame

pygame.mixer.init()


class GameState:
    def __init__(self):
        self.board_obj = Board()  # Board instance
        self.selected_pos = None
        self.highlighted_moves = []
        self.turn_counter = 0
        self.captured_white = []  # black pieces captured by white
        self.captured_black = []  # white pieces captured by black
        self.captured_sound = pygame.mixer.Sound('sound/capture.mp3')
        self.moving_sound = pygame.mixer.Sound('sound/move.mp3')
        self.check_notification = pygame.mixer.Sound('sound/check_notification.mp3')
        self.checkmate_sound = pygame.mixer.Sound('sound/checkmate.mp3')
        self.w_king_pos = (7, 4)
        self.b_king_pos = (0, 4)
        self.w_check = False
        self.b_check = False
        self.b_wins = False
        self.w_wins = False
        self.promoting = False
        self.promotion_pos = None
        self.promotion_color = None

    def handle_click(self, x, y, board):
        row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

        if not (0 <= row < 8 and 0 <= col < 8):
            return

        clicked_piece = board[row][col]
        current_turn = self.turn()

        if clicked_piece != '.' and clicked_piece.color == current_turn:
            self.select_piece(clicked_piece, board)

        elif self.selected_pos and (row, col) in self.highlighted_moves:
            self.move_piece(board, row, col)

        else:
            self.clear_selection()

    def move_piece(self, board, dest_row, dest_col):
        src_row, src_col = self.selected_pos
        piece = board[src_row][src_col]
        target = board[dest_row][dest_col]

        # Capture logic
        if target != '.':
            self.captured_sound.play()
            if target.color == 'w':
                self.captured_black.append(target)
            else:
                self.captured_white.append(target)

        # Move piece
        board[dest_row][dest_col] = piece
        if piece.__repr__() == 'king_w':
            self.w_king_pos = (dest_row, dest_col)
        elif piece.__repr__() == 'king_b':
            self.b_king_pos = (dest_row, dest_col)
        board[src_row][src_col] = '.'
        piece.row, piece.col = dest_row, dest_col
        if isinstance(piece, Pawn):
            if piece.check_promotion():
                # Ask for promotion piece (stub function for now)
                self.promoting = True
                self.promotion_pos = (dest_row, dest_col)
                self.promotion_color = piece.color
        self.moving_sound.play()

        self.check_checker(board)

        if not self.promoting:
            self.turn_counter += 1
            self.clear_selection()
        print(f"Moved {piece} to ({dest_row}, {dest_col}) — Turn: {self.turn_counter}")
        print(f'White king pos: {self.w_king_pos}')
        print(f'Black king pos: {self.b_king_pos}')

    def clear_selection(self):
        self.selected_pos = None
        self.highlighted_moves = []

    def turn(self):
        return 'w' if self.turn_counter % 2 == 0 else 'b'

    def check_checker(self, board):
        self.w_check = self.is_king_in_check(board, 'w', self.w_king_pos)
        self.b_check = self.is_king_in_check(board, 'b', self.b_king_pos)

        if self.w_check or self.b_check:
            self.check_notification.play()

        self.checkmate_checker(board)

    def is_king_in_check(self, board, king_color, king_pos):
        for row in board:
            for piece in row:
                if piece != '.' and piece.color != king_color:
                    if king_pos in piece.current_possible_moves(board):
                        return True
        return False

    def get_legal_moves(self, piece, board):
        legal_moves = []
        possible_moves = piece.current_possible_moves(board)
        original_row, original_col = piece.row, piece.col

        for move_row, move_col in possible_moves:
            # Backup destination square
            captured_piece = board[move_row][move_col]

            # Simulate move
            board[original_row][original_col] = '.'
            board[move_row][move_col] = piece
            piece.row, piece.col = move_row, move_col

            # Track king position
            king_pos = self.w_king_pos if piece.color == 'w' else self.b_king_pos
            if piece.__repr__() == f'king_{piece.color}':
                king_pos = (move_row, move_col)

            # Check if move would put own king in check
            in_check = self.is_king_in_check(board, piece.color, king_pos)

            # Undo move
            board[move_row][move_col] = captured_piece
            board[original_row][original_col] = piece
            piece.row, piece.col = original_row, original_col

            if not in_check:
                legal_moves.append((move_row, move_col))

        return legal_moves

    def select_piece(self, piece, board):
        self.selected_pos = (piece.row, piece.col)
        self.highlighted_moves = self.get_legal_moves(piece, board)
        print(f"Selected {piece}, possible moves: {self.highlighted_moves}")

    def checkmate_checker(self, board):
        if self.w_check:
            color_in_check = 'w'
            king_pos = self.w_king_pos
        elif self.b_check:
            color_in_check = 'b'
            king_pos = self.b_king_pos
        else:
            return  # No check, so no checkmate

        for row in board:
            for piece in row:
                if piece != '.' and piece.color == color_in_check:
                    possible_moves = self.get_legal_moves(piece, board)
                    for move in possible_moves:
                        # Simulate move
                        backup_piece = board[move[0]][move[1]]
                        orig_row, orig_col = piece.row, piece.col

                        board[move[0]][move[1]] = piece
                        board[orig_row][orig_col] = '.'
                        piece.row, piece.col = move

                        temp_king_pos = king_pos
                        if piece.__repr__() == f'king_{color_in_check}':
                            temp_king_pos = move

                        if not self.is_king_in_check(board, color_in_check, temp_king_pos):
                            # Undo
                            board[move[0]][move[1]] = backup_piece
                            board[orig_row][orig_col] = piece
                            piece.row, piece.col = orig_row, orig_col
                            return  # Found escape

                        # Undo
                        board[move[0]][move[1]] = backup_piece
                        board[orig_row][orig_col] = piece
                        piece.row, piece.col = orig_row, orig_col

        # If loop completes, it's checkmate
        self.checkmate_sound.play()
        if color_in_check == 'w':
            self.b_wins = True
        else:
            self.w_wins = True

    def promote_piece(self, choice, row, col, color):
        if choice == 'queen':
            return Queen(row, col, color)
        elif choice == 'rook':
            return Rook(row, col, color)
        elif choice == 'bishop':
            return Bishop(row, col, color)
        elif choice == 'knight':
            return Knight(row, col, color)
        else:
            return Queen(row, col, color)  # default fallback

    def handle_promotion_click(self, mouse_pos, scaled_images, color):
        """Handle the click on the promotion menu and return the selected piece."""
        for scaled_image, image_rect, piece_name in scaled_images:
            if image_rect.collidepoint(mouse_pos):
                return piece_name
        return None

    def promote_pawn(self, selected_piece):
        """Promote the selected pawn to the selected piece (e.g., Queen, Rook, etc.)."""
        if self.promotion_pos:
            row, col = self.promotion_pos
            piece_class = None
            if selected_piece == 'queen':
                piece_class = Queen  # Assuming you have a Queen class
            elif selected_piece == 'rook':
                piece_class = Rook  # Assuming you have a Rook class
            elif selected_piece == 'bishop':
                piece_class = Bishop  # Assuming you have a Bishop class
            elif selected_piece == 'knight':
                piece_class = Knight  # Assuming you have a Knight class

            # Replace the pawn with the new piece
            self.board_obj.board[row][col] = piece_class(row, col, self.promotion_color)
            self.check_checker(self.board_obj.board)  # to check for check if there is
            # Perform any other necessary updates (e.g., remove the pawn from the list)
            self.promotion_pos = None
            self.promoting = False
            self.promotion_color = None

    def draw_highlighted_moves(self, win, square_size):
        dot_color = (192, 192, 192)
        dot_radius = square_size // 6
        if self.selected_pos:
            for row, col in self.highlighted_moves:
                center_x = col * square_size + square_size // 2
                center_y = row * square_size + square_size // 2
                pygame.draw.circle(win, dot_color, (center_x, center_y), dot_radius)
