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
        self.board_display_size = 800  # Size of the board display area (800x800)
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

Config = setting()
