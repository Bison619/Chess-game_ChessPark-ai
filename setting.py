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

Config = setting()