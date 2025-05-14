import pygame


class SoundManager:
    """
    Manages all game sound effects for moves, captures, checks, and checkmates.
    """

    def __init__(self):
        self.capture_sound = pygame.mixer.Sound("sound/capture.mp3")
        self.move_sound = pygame.mixer.Sound("sound/move.mp3")
        self.check_notification = pygame.mixer.Sound('sound/check_notification.mp3')
        self.checkmate_sound = pygame.mixer.Sound('sound/checkmate.mp3')

    def play_capture(self):
        self.capture_sound.play()

    def play_move(self):
        self.move_sound.play()

    def play_check_notification(self):
        self.check_notification.play()

    def play_checkmate_sound(self):
        self.checkmate_sound.play()
