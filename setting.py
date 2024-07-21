import pygame

pygame.init()
pygame.font.init()

class setting:
    def __init__(self):
        self.boardSize = 8
        self.width = 1600
        self.height = 900
        self.resolution = (self.width, self.height)
        self.fps = 60
        self.board_display_size = 800
        self.spotSize = self.board_display_size // self.boardSize
        self.top_offset = (self.height - self.board_display_size) // 2
        self.horizontal_offset = (self.width - self.board_display_size) // 2
        self.CoordFont = pygame.font.SysFont("jaapokki", 18, bold=True)
        self.highlightOutline = 5
        self.themeIndex = -1
        self.themes = [
            # BROWN THEME
            {"dark": (165, 117, 80), "light": (235, 209, 166), "outline": (0, 0, 0)},
            # BLUE THEME
            {"dark": (60, 95, 135), "light": (229, 228, 200), "outline": (0, 0, 0)},
            # GRAY THEME
            {"dark": (86, 85, 84), "light": (120, 119, 118), "outline": (0, 0, 0)},
            # GREEN THEME
            {"dark": (119, 154, 88), "light": (234, 235, 200), "outline": (0, 0, 0)},
        ]

class Sound:
    def __init__(self):
        self.capture_sound = pygame.mixer.Sound("./assets/sounds/capture.mp3")
        self.castle_sound = pygame.mixer.Sound("./assets/sounds/castle.mp3")
        self.check_sound = pygame.mixer.Sound("./assets/sounds/Check.mp3")
        self.button_sound = pygame.mixer.Sound("./assets/sounds/button-sound.mp3")
        self.checkmatewin_sound = pygame.mixer.Sound("./assets/sounds/Checkmate_Win.mp3")
        self.checkmatelose_sound = pygame.mixer.Sound("./assets/sounds/Checkmate_Lose.mp3")
        self.game_over_sound = pygame.mixer.Sound("./assets/sounds/game-end.mp3")
        self.game_start_sound = pygame.mixer.Sound("./assets/sounds/game-start.mp3")
        self.move_sound = pygame.mixer.Sound("./assets/sounds/move-self.mp3")
        # self.stalemate_sound = pygame.mixer.Sound("./assets/sounds/stalemate_sound.mp3")
        self.promote_sound = pygame.mixer.Sound("./assets/sounds/promote.mp3")

Config = setting()
sounds = Sound()
