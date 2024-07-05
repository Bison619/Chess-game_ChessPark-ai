import pygame

pygame.init()
pygame.font.init()

class setting:
    def __init__(self):
        self.boardSize = 8
        self.width = 1600
        self.height = 900
        self.resolution = (self.width,self.height)
        self.fps = 60
        self.top_offset = 10
        self.spotSize = (self.height - self.top_offset) // self.boardSize
        self.horizontal_offset = self.width // 2 - (self.spotSize * (self.boardSize // 2))
        self.CoordFont = pygame.font.SysFont("jaapokki", 18, bold=True)
        self.highlightOutline = 5
        self.themeIndex = -1
        self.themes = [
            # CORAL THEME
            {"dark": (112, 162, 163), "light": (173, 228, 185), "outline": (0, 0, 0)},
            # DUSK THEME
            {"dark": (112, 102, 119), "light": (204, 183, 174), "outline": (0, 0, 0)},
            # MARINE THEME
            {"dark": (111, 115, 210), "light": (157, 172, 255), "outline": (0, 0, 0)},
            # WHEAT THEME
            {"dark": (187, 190, 100), "light": (234, 240, 206), "outline": (0, 0, 0)},
            # EMERALD THEME
            {"dark": (111, 143, 114), "light": (173, 189, 143), "outline": (0, 0, 0)},
            # SAND CASTLE THEME
            {"dark": (184, 139, 74), "light": (227, 193, 111), "outline": (0, 0, 0)},
            # CHESS.com THEME
            {"dark": (148, 111, 81), "light": (240, 217, 181), "outline": (0, 0, 0)},
            # GREEN THEME
            {"dark": (118, 148, 85), "light": (234, 238, 210), "outline": (0, 0, 0)},
        ]

Config = setting()