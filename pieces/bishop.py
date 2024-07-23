from pieces.base import Piece
from tools import OnBoard, Position
from setting import Config
from utils import GetSprite

class Bishop(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "b"
        self.value = 3 if color == 0 else -3
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.pieceMap = []

    def GetMoves(self, board):
        moves, captures = self.DiagonalMoves(board)
        return moves, captures

    def DiagonalMoves(self, board):
        patterns = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        moves, captures = self.GetPatternMoves(board, patterns)
        return moves, captures
