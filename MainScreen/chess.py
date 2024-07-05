import pygame
import sys
import time

import ui
from setting import Config

class Chess:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.gameOver = False
        self.animateSpot = 1

    def GetFrameRate(self):
        return self.clock.get_fps()

    def vsPlayer(self):
        pygame.event.clear()
        while not self.gameOver:
            self.clock.tick(Config.fps)
            self.screen.fill((0, 0, 0))
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
            pass
        self.DrawChessCoordinate()

    def DrawChessBoard(self):
        if self.animateSpot < Config.spotSize:
            self.animateSpot += 2
        for i in range(Config.boardSize):
            for j in range(Config.boardSize):
                x = i * Config.spotSize + Config.horizontal_offset
                y = j * Config.spotSize + Config.top_offset // 2
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.screen, Config.themes[Config.themeIndex]["light"], [x, y, self.animateSpot, self.animateSpot])
                else:
                    pygame.draw.rect(self.screen, Config.themes[Config.themeIndex]["dark"], [x, y, self.animateSpot, self.animateSpot])

    def DrawChessCoordinate(self):
        for i in range(Config.boardSize):
            _x = 0.05 * Config.spotSize + Config.horizontal_offset
            _y = 0.05 * Config.spotSize + Config.top_offset + i * Config.spotSize
            color = Config.themes[Config.themeIndex]['dark'] if i % 2 == 0 else Config.themes[Config.themeIndex]['light']

            fontRenderer = Config.CoordFont.render(str(8-i), True, color)
            self.screen.blit(fontRenderer, (_x, _y))

            _x = 0.9 * Config.spotSize + Config.horizontal_offset + i * Config.spotSize
            _y = (Config.boardSize - 1) * Config.spotSize + Config.top_offset + Config.spotSize * 0.75
            color = Config.themes[Config.themeIndex]['light'] if i % 2 == 0 else Config.themes[Config.themeIndex]['dark']

            fontRenderer = Config.CoordFont.render(chr(ord("a")+ i), True, color)
            self.screen.blit(fontRenderer, (_x, _y))
