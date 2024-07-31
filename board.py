import pygame
import time
import random
from pieces import *
from setting import Config, sounds
from tools import Position, OnBoard
import math
from Fen import *

class Board:
    def __init__(self):
        # # 0 -> white , 1 -> Black
        # self.player = random.choice([0, 1])
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
        self.moveLog = []
        self.captured_white_pieces = []
        self.captured_black_pieces = []


    def get_piece_from_code(self, code, color, position):
        pieces = {
            'p': Pawn,
            'r': Rook,
            'n': Knight,
            'b': Bishop,
            'q': Queen,
            'k': King
        }
        piece_class = pieces.get(code.lower())
        if piece_class:
            return piece_class(position, color)
        return None

    def Forfeit(self):
        # Resign
        self.winner = 1 if self.player == 0 else 0
        # self.DisplayWinner()

    # def DisplayWinner(self):
    #         if self.winner is not None:
    #             sounds.button_sound.play()
    #             self.screen.blit(self.gameOverBackground, (0, 0))
    #             self.gameOverHeader.Draw()

    #         if self.player == 0:
    #                 self.winnerText.text = "Black wins by resignation!"
    #                 king_image = self.board.WhiteKing.sprite
    #                 scaled_king_image = pygame.transform.scale(king_image, (king_image.get_width() + 20, king_image.get_height() + 20))
    #                 self.screen.blit(scaled_king_image, (Config.width // 2 - Config.spotSize // 2, Config.height // 3 - 50))
    #         elif self.player == 1:
    #                 self.winnerText.text = "White wins by resignation!"
    #                 king_image = self.board.BlackKing.sprite
    #                 scaled_king_image = pygame.transform.scale(king_image, (king_image.get_width() + 20, king_image.get_height() + 20))
    #                 self.screen.blit(scaled_king_image, (Config.width // 2 - Config.spotSize // 2, Config.height // 3 - 50))

    #         self.gameOverHeader.Draw()
    #         self.winnerText.Draw()
    #         pygame.display.update()
    #         time.sleep(5)
    #         self.board = Board()
    #         self.animateSpot = 1

    def GetPiece(self, coord):
        return self.grid[coord.x][coord.y]

    def SetPiece(self, position, piece):
        self.grid[position.x][position.y] = piece

    def SwitchTurn(self):
        # switch between 0 and 1
        # (0 + 1) * -1 + 2 = 1
        # (1 + 1) * -1 + 2 = 0
        self.player = (self.player + 1 ) * -1 + 2
        # CHECK IF THE PLAYER LOST OR NOT
        self.IsCheckmate()

    def RecentMove(self):
        return None if not self.historic else self.historic[-1]

    def RecentMovePositions(self):
        if not self.historic or len(self.historic) <= 1:
            return None, None
        pos = self.historic[-1][3]
        oldPos = self.historic[-1][4]

        return pos.GetCopy(), oldPos.GetCopy()

    def AllowedMoveList(self, piece, moves, isAI):
        allowed_moves = []
        for move in moves:
            if self.VerifyMove(piece, move.GetCopy(), isAI):
                allowed_moves.append(move.GetCopy())
        return allowed_moves

    def GetAllowedMoves(self, piece, isAI=False):
        moves, captures = piece.GetMoves(self)
        allowed_moves = self.AllowedMoveList(piece, moves.copy(), isAI)
        allowed_captures = self.AllowedMoveList(piece, captures.copy(), isAI)
        return allowed_moves, allowed_captures

    def Move(self, piece, position):
        if position != None:
            position = position.GetCopy()
            # print(position)
            if self.isCastling(piece, position.GetCopy()):
                self.CastleKing(piece, position.GetCopy())
            elif self.isEnPassant(piece, position.GetCopy()):
                self.grid[position.x][piece.position.y] = None
                self.MovePiece(piece, position)
                self.historic[-1][2] = piece.code + " EP"
            else:
                self.MovePiece(piece, position)
            # check for promotion
            if type(piece) == Pawn and (piece.position.y == 0 or piece.position.y == 7):
                self.pieceToPromote = piece
            else:
                self.SwitchTurn()
            self.Check()

    def MovePiece(self, piece, position):
        position = position.GetCopy()
        old_position = piece.position.GetCopy()
        self.grid[old_position.x][old_position.y] = None
        piece.updatePosition(position)
        self.grid[position.x][position.y] = piece
        self.historic.append([self.moveIndex, piece.color, piece.code, old_position, piece.position, piece])
        piece.previousMove = self.moveIndex
        self.moveIndex += 1
        self.checkBlackKing = False
        self.checkWhiteKing = False
        # Add the move to the move log
        piece_notation = {
            "Pawn": "P",
            "Knight": "Kn",
            "Bishop": "B",
            "Rook": "R",
            "Queen": "Q",
            "King": "K"
        }

        piece_name = piece.__class__.__name__
        move = f"{piece_notation.get(piece_name, '')}{chr(position.x + 97)}{8 - position.y}{','}"
        self.moveLog.append(move)

    def VerifyMove(self, piece, move, isAI):
        # verify the move by going through all the possible outcomes
        # This function will return False if the opponent will reply by capturing the king
        position = move.GetCopy()
        oldPosition = piece.position.GetCopy()
        captureEnPassant = None
        # print(f"new: {move}, old: {oldPosition}")
        capturedPiece = self.grid[position.x][position.y]
        if self.isEnPassant(piece, position):
            captureEnPassant = self.grid[position.x][oldPosition.y]
            self.grid[position.x][oldPosition.y] = None

        self.grid[oldPosition.x][oldPosition.y] = None
        self.grid[position.x][position.y] = piece
        # print(f"pos: {position}, old: {oldPosition}")
        piece.updatePosition(move)
        EnemyCaptures = self.GetEnemyCaptures(self.player)
        if self.isCastling(piece, oldPosition):
            if math.fabs(position.x - oldPosition.x) == 2 and not self.VerifyMove(piece, Position(5, position.y), isAI) \
                or math.fabs(position.x - oldPosition.x) == 3 and not self.VerifyMove(piece, Position(3, position.y), isAI) \
                or self.IsInCheck(piece):
                self.UndoMove(piece, capturedPiece, oldPosition, position)
                return False

        for pos in EnemyCaptures:
            if (self.WhiteKing.position == pos and piece.color == 0) \
                or (self.BlackKing.position == pos and piece.color == 1):
                self.UndoMove(piece, capturedPiece, oldPosition, position)
                if captureEnPassant != None:
                    self.grid[position.x][oldPosition.y] = captureEnPassant
                return False
        self.UndoMove(piece, capturedPiece, oldPosition, position)
        if captureEnPassant != None:
            self.grid[position.x][oldPosition.y] = captureEnPassant
        return True

    def UndoMove(self, piece, captured, oldPos, pos):
        self.grid[oldPos.x][oldPos.y] = piece
        self.grid[pos.x][pos.y] = captured
        piece.updatePosition(oldPos)

    def GetEnemyCaptures(self, player):
        captures = []
        for pieces in self.grid:
            for piece in pieces:
                if piece != None and piece.color != player:
                    moves, piececaptures = piece.GetMoves(self)
                    captures = captures + piececaptures
        return captures

    def isCastling(self,king, position):
        return type(king) == King and abs(king.position.x - position.x) > 1

    def isEnPassant(self, piece, newPos):
        if type(piece) != Pawn:
            return False
        moves = None
        if piece.color == 0:
            moves = piece.EnPassant(self, -1)
        else:
            moves = piece.EnPassant(self, 1)
        return newPos in moves

    def IsInCheck(self, piece):
        return type(piece) == King and \
                ((piece.color == 0 and self.checkWhiteKing) or (piece.color == 1 and self.checkBlackKing))

    def CastleKing(self, king, position):
        position = position.GetCopy()
        # print("castled")
        # print(position)
        if position.x == 2 or position.x == 6:
            if position.x == 2:
                rook = self.grid[0][king.position.y]
                self.MovePiece(king, position)
                self.grid[0][rook.position.y] = None
                rook.position.x = 3
                # print("black castled")
            else:
                rook = self.grid[7][king.position.y]
                self.MovePiece(king, position)
                self.grid[7][rook.position.y] = None
                rook.position.x = 5
                # print("white castled")

            rook.previousMove = self.moveIndex - 1
            self.grid[rook.position.x][rook.position.y] = rook
            self.historic[-1][2] = king.code + " C"
            sounds.castle_sound.play()

    def PromotePawn(self, pawn, choice):
        if choice == 0:
            self.grid[pawn.position.x][pawn.position.y] = Queen(pawn.position.GetCopy(), pawn.color)
        elif choice == 1:
            self.grid[pawn.position.x][pawn.position.y] = Bishop(pawn.position.GetCopy(), pawn.color)
        elif choice == 2:
            self.grid[pawn.position.x][pawn.position.y] = Knight(pawn.position.GetCopy(), pawn.color)
        elif choice == 3:
            self.grid[pawn.position.x][pawn.position.y] = Rook(pawn.position.GetCopy(), pawn.color)

        self.SwitchTurn()
        self.Check()
        self.pieceToPromote = None

    def MoveSimulation(self, piece, next_pos):
        if self.grid[next_pos.x][next_pos.y] == None:
            self.grid[piece.position.x][piece.position.y] = None
            piece.position = next_pos.GetCopy()
            self.grid[next_pos.x][next_pos.y] = piece
            return None
        else:
            prev_piece = self.grid[next_pos.x][next_pos.y]
            self.grid[piece.position.x][piece.position.y] = None
            piece.position = next_pos.GetCopy()
            self.grid[next_pos.x][next_pos.y] = piece
            return prev_piece

    def Check(self):
        if self.player == 0:
            king = self.WhiteKing
        else:
            king = self.BlackKing

        for pieces in self.grid:
            for piece in pieces:
                if piece != None and piece.color != self.player:
                    moves, captures = self.GetAllowedMoves(piece)
                    if king.position in captures:
                        if self.player == 1:
                            self.checkBlackKing = True
                            sounds.check_sound.play()
                            return
                        else:
                            self.checkWhiteKing = True
                            sounds.check_sound.play()
                            return

    def IsCheckmate(self):
        for pieces in self.grid:
            for piece in pieces:
                if piece != None and piece.color == self.player:
                    moves, captures = self.GetAllowedMoves(piece)
                    # if there's any legal move left
                    # then it's not checkmate
                    if moves or captures:
                        return False
        self.Check()
        if self.checkWhiteKing:
            # black won
            self.winner = 1
        elif self.checkBlackKing:
            # white won
            self.winner = 0
        else:
            # it's a ----------
            self.winner = -1
        return True
