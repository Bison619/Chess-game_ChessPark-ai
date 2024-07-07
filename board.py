import pygame
from pieces import *
from setting import Config
from tools import Position, OnBoard
import math
from Fen import *

class Board:
    def __init__(self):
        # 0 -> white , 1 -> Black
        self.player = 0
        self.historic = []
        self.moveIndex = 1
        self.font = pygame.font.SysFont("Consolas", 18, bold=True)
        self.grid = FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        self.WhiteKing = None
        self.BlackKing = None
        for pieces in self.grid:
            for piece in pieces:
                if piece != None:
                    if piece.color == 0 and piece.code == "k":
                        self.WhiteKing = piece
                    elif piece.color == 1 and piece.code == "k":
                        self.BlackKing = piece

        self.checkWhiteKing = False
        self.checkBlackKing = False

        self.winner = None
        self.pieceToPromote = None

        self.whitePromotions = [Queen(Position(0, 0), 0), Bishop(Position(0, 1), 0), Knight(Position(0, 2), 0), Rook(Position(0, 3), 0)]
        self.blackPromotions = [Rook(Position(0, 7), 1), Knight(Position(0, 6), 1), Bishop(Position(0, 5), 1), Queen(Position(0, 4), 1)]

    def Forfeit(self):
        # resign
        pass

    def GetPiece(self, coord):
        return self.grid[coord.x][coord.y]

    def SetPiece(self, position, piece):
        self.grid[position.x][position.y] = piece