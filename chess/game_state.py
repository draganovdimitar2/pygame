from chess.pieces.queen import Queen
from chess.pieces.rook import Rook
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.board import Board
from chess.pieces.pawn import Pawn
from chess.pieces.king import King
from chess.settings import SQUARE_SIZE
import pygame

pygame.mixer.init()


class GameState:
    def __init__(self):
        self.board_obj = Board()  # board instance
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

        # check if it's a king's move for castling
        if isinstance(piece, King) and abs(dest_col - src_col) == 2:  # castling move (king moves 2 squares)
            # we need to check if the castling conditions are met here
            self.castling(board, piece, dest_col)  # this handles the castling logic
            piece.row, piece.col = dest_row, dest_col
            if piece.color == 'w':
                self.w_king_pos = (dest_row, dest_col)
            else:
                self.b_king_pos = (dest_row, dest_col)
            board[dest_row][dest_col] = piece
            board[src_row][src_col] = '.'
            self.moving_sound.play()
            self.turn_counter += 1
            self.clear_selection()
            self.check_checker(board)
            return  # return here to prevent further piece movement

        if isinstance(piece, Pawn) and (
                (piece.color == 'w' and dest_row == 0) or (piece.color == 'b' and dest_row == 7)):
            self.promoting = True
            self.promotion_pos = (dest_row, dest_col)
            self.promotion_color = piece.color
            board[dest_row][dest_col] = piece  # move the pawn to promotion square
            board[src_row][src_col] = '.'
            return

        # continue with normal piece move logic
        # Check for capture
        captured = board[dest_row][dest_col]
        if captured != '.' and captured.color != piece.color:
            if captured.color == 'w':
                self.captured_white.append(captured)
            else:
                self.captured_black.append(captured)
            self.captured_sound.play()
        else:
            self.moving_sound.play()

        # Move the piece
        board[dest_row][dest_col] = piece
        piece.row, piece.col = dest_row, dest_col
        if isinstance(piece, King):  # update king pos
            if piece.color == 'w':
                self.w_king_pos = (dest_row, dest_col)
            else:
                self.b_king_pos = (dest_row, dest_col)
        if isinstance(piece, (King, Rook)):  # castling check
            piece.has_moved = True

        board[src_row][src_col] = '.'
        self.moving_sound.play()
        self.check_checker(board)

        self.turn_counter += 1
        self.clear_selection()

    def castling_check(self, board, piece, side):
        if not isinstance(piece, King) or piece.has_moved:
            return False

        row = 0 if piece.color == 'b' else 7
        if side == 'kingside':
            rook_col = 7
            between_cols = [5, 6]
            king_target_col = 6
        elif side == 'queenside':
            rook_col = 0
            between_cols = [1, 2, 3]
            king_target_col = 2
        else:
            return False

        # check if squares between king and rook are empty
        for col in between_cols:
            if board[row][col] != '.':
                return False

        # check rook conditions
        rook = board[row][rook_col]
        if not isinstance(rook, Rook) or rook.has_moved or rook.color != piece.color:
            return False

        # check king is not in check, and doesn't pass through check
        if (self.w_check and piece.color == 'w') or (self.b_check and piece.color == 'b'):
            return False

        for col in [4, king_target_col]:  # Check current and destination square
            if piece.would_be_in_check(board, row, col):
                return False

        return True

    def castling(self, board, king, target_col):
        row = king.row

        # only proceed if it's a 2-square horizontal move (possible castling)
        if abs(king.col - target_col) != 2:
            print("Invalid castling move.")
            return False

        if target_col > king.col:
            # kingside castling
            rook_col = 7
            rook_target_col = 5
            path_cols = range(king.col + 1, rook_col)
        else:
            # queenside castling
            rook_col = 0
            rook_target_col = 3
            path_cols = range(rook_col + 1, king.col)

        # check path is clear
        for col in path_cols:
            if board[row][col] != '.':
                print(f"Path blocked for castling at ({row}, {col})")
                return False

        # validate rook
        rook = board[row][rook_col]
        if not isinstance(rook, Rook) or rook.has_moved:
            print("Castling blocked or rook already moved.")
            return False

        # move the king
        board[row][target_col] = king
        board[row][king.col] = '.'
        king.col = target_col
        king.has_moved = True

        # move the rook
        board[row][rook_target_col] = rook
        board[row][rook_col] = '.'
        rook.col = rook_target_col
        rook.has_moved = True

        print(f"Castling completed for {king.color} king to ({row}, {target_col})")
        return True

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

        # add castling moves if piece is king
        if isinstance(piece, King):
            row = 0 if piece.color == 'b' else 7

            # kingside castling
            if self.castling_check(board, piece, 'kingside'):
                legal_moves.append((row, 6))  # g1 / g8

            # queenside castling
            if self.castling_check(board, piece, 'queenside'):
                legal_moves.append((row, 2))  # c1 / c8

        for move_row, move_col in possible_moves:
            # backup destination square
            captured_piece = board[move_row][move_col]

            # simulate move
            board[original_row][original_col] = '.'
            board[move_row][move_col] = piece
            piece.row, piece.col = move_row, move_col

            # track king position
            king_pos = self.w_king_pos if piece.color == 'w' else self.b_king_pos
            if piece.__repr__() == f'king_{piece.color}':
                king_pos = (move_row, move_col)

            # check if move would put own king in check
            in_check = self.is_king_in_check(board, piece.color, king_pos)

            # undo move
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
            return  # no check, so no checkmate

        for row in board:
            for piece in row:
                if piece != '.' and piece.color == color_in_check:
                    possible_moves = self.get_legal_moves(piece, board)
                    for move in possible_moves:
                        # simulate move
                        backup_piece = board[move[0]][move[1]]
                        orig_row, orig_col = piece.row, piece.col

                        board[move[0]][move[1]] = piece
                        board[orig_row][orig_col] = '.'
                        piece.row, piece.col = move

                        temp_king_pos = king_pos
                        if piece.__repr__() == f'king_{color_in_check}':
                            temp_king_pos = move

                        if not self.is_king_in_check(board, color_in_check, temp_king_pos):
                            # undo
                            board[move[0]][move[1]] = backup_piece
                            board[orig_row][orig_col] = piece
                            piece.row, piece.col = orig_row, orig_col
                            return  # found escape

                        # undo
                        board[move[0]][move[1]] = backup_piece
                        board[orig_row][orig_col] = piece
                        piece.row, piece.col = orig_row, orig_col

        # if loop completes, it's checkmate
        self.checkmate_sound.play()
        if color_in_check == 'w':
            self.b_wins = True
        else:
            self.w_wins = True

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
                piece_class = Queen
            elif selected_piece == 'rook':
                piece_class = Rook
            elif selected_piece == 'bishop':
                piece_class = Bishop
            elif selected_piece == 'knight':
                piece_class = Knight

                # replace the pawn with the new piece
            self.board_obj.board[row][col] = piece_class(row, col, self.promotion_color)
            self.check_checker(self.board_obj.board)  # to check for check if there is
            # perform other updates
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
