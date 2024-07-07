import pygame
import sys
import time

from setting import Config
from utils import GetSprite
from board import Board
import ui

class Chess:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.gameOver = False
        self.animateSpot = 5
        self.board = Board()
        self.background = pygame.image.load("./assets/images/mainbg2blur.png")
        self.background = pygame.transform.scale(self.background, Config.resolution)

    def GetFrameRate(self):
        return self.clock.get_fps()

    def vsPlayer(self):
        pygame.event.clear()
        while not self.gameOver:
            self.clock.tick(Config.fps)
            self.background = pygame.image.load("./assets/images/mainbg2blur.png")
            self.HandleEvents()
            self.Render()
            pygame.display.set_caption("Chess : VS Player " + str(int(self.GetFrameRate())))
            pygame.display.update()

    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameOver = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.gameOver = True
                if event.key == pygame.K_UP:
                    if Config.themeIndex < len(Config.themes) -1:
                        Config.themeIndex += 1
                    else:
                        Config.themeIndex = 0
                if event.key == pygame.K_DOWN:
                    if Config.themeIndex > 0:
                        Config.themeIndex -= 1
                    else:
                        Config.themeIndex = len(Config.themes) -1

    def Render(self):
        self.DrawChessBoard()
        if self.animateSpot >= Config.spotSize:
            self.DrawPieces()
        self.DrawChessCoordinate()

    def DrawChessBoard(self):
        if self.animateSpot < Config.spotSize:
            self.animateSpot += 5

        for i in range(Config.boardSize):
            for j in range(Config.boardSize):
                x = i * Config.spotSize + Config.horizontal_offset
                y = j * Config.spotSize + Config.top_offset

                if (i + j) % 2 == 0:
                    color = Config.themes[Config.themeIndex]["light"]
                else:
                    color = Config.themes[Config.themeIndex]["dark"]

                pygame.draw.rect(self.screen, color, [x, y, self.animateSpot, self.animateSpot])

    def DrawChessCoordinate(self):
        for i in range(Config.boardSize):
            # Row numbers on the left side
            x = Config.horizontal_offset
            y = i * Config.spotSize + Config.top_offset + Config.spotSize - 20
            color = Config.themes[Config.themeIndex]['dark'] if (i % 2) == 0 else Config.themes[Config.themeIndex]['light']
            fontRenderer = Config.CoordFont.render(str(Config.boardSize - i), True, color)
            self.screen.blit(fontRenderer, (x, y))

            # Column letters at the bottom
            x = i * Config.spotSize + Config.horizontal_offset + 90
            y = Config.top_offset + Config.board_display_size - 15
            color = Config.themes[Config.themeIndex]['light'] if (i % 2) == 0 else Config.themes[Config.themeIndex]['dark']
            fontRenderer = Config.CoordFont.render(chr(ord("a") + i), True, color)
            self.screen.blit(fontRenderer, (x, y))

    def DrawPieces(self):
        # Loop through the board grid and draw each piece on the screen
        for x in range(Config.boardSize):
            for y in range(Config.boardSize):
                x_pos = x * Config.spotSize + Config.horizontal_offset
                y_pos = y * Config.spotSize + Config.top_offset
                piece = self.board.grid[x][y]
                if piece is not None:
                    sprite = GetSprite(piece)
                    self.screen.blit(sprite, (x_pos, y_pos))
