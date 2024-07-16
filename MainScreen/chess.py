import pygame
import sys
import time

from setting import Config, sounds
from tools import Position, OnBoard
from utils import GetSprite, bh, oh, ch ,rh
from board import Board
from ui import Button

class Chess:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.piece_size = 40
        self.board = Board()
        self.gameOver = False
        self.animateSpot = 5
        self.selectedPiece = None
        self.selectedPieceMoves = None
        self.selectedPieceCaptures = None
        self.draggedPiece = None
        self.CanBeReleased = False
        self.AdjustedMouse = Position(0, 0)
        self.background = pygame.image.load("./assets/images/mainbg2blur.png")
        self.background = pygame.transform.scale(self.background, Config.resolution)
        self.moveLogFont = pygame.font.SysFont("Verdana", 18)

    def GetFrameRate(self):
        return self.clock.get_fps()

    def vsPlayer(self):
        pygame.event.clear()
        while not self.gameOver:
            self.clock.tick(Config.fps)
            self.background = pygame.image.load("./assets/images/mainbg2blur.png")
            self.getMousePosition()
            pygame.display.set_caption("Chess : VS Player " + str(int(self.GetFrameRate())))
            self.display()
            if self.animateSpot >= Config.spotSize:
                self.HandleEvents()
            pass

    def display(self):
        self.Render()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # print(self.AdjustedMouse)
                    self.HandleOnLeftMouseButtonDown()
                elif event.button == 3:
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.HandleOnLeftMouseButtonUp()

    def HandleOnLeftMouseButtonUp(self):
        self.draggedPiece = None
        if self.selectedPiece:
            if self.selectedOrigin != self.AdjustedMouse:
                if self.AdjustedMouse in self.selectedPieceCaptures:
                    self.board.Move(self.selectedPiece, self.AdjustedMouse)
                    # play sounds
                    sounds.capture_sound.play()
                elif self.AdjustedMouse in self.selectedPieceMoves :
                    self.board.Move(self.selectedPiece, self.AdjustedMouse)
                    # play sound
                    sounds.move_sound.play()
                self.ReleasePiece()
            elif self.CanBeReleased:
                self.ReleasePiece()
            else:
                self.CanBeReleased = True

    def SelectPiece(self,piece):
        if piece != None and piece.color == self.board.player:
            self.selectedPiece = piece
            self.draggedPiece = piece
            self.selectedPieceMoves, self.selectedPieceCaptures = self.board.GetAllowedMoves(self.selectedPiece)
            # self.selectedPieceMoves, self.selectedPieceCaptures = piece.GetMoves(self.board)
            self.selectedOrigin = self.AdjustedMouse


    def HandleOnLeftMouseButtonDown(self):
        if self.board.pieceToPromote != None and self.AdjustedMouse.x == self.board.pieceToPromote.position.x:
            choice = self.AdjustedMouse.y
            if choice <= 3 and self.board.player == 0:
                # promote pawn
                self.board.PromotePawn(self.board.pieceToPromote, choice)
                # refresh screen
                self.display()
            elif choice > 3 and self.board.player == 1:
                # promote pawn
                self.board.PromotePawn(self.board.pieceToPromote, 7-choice)
                # refresh screen
                self.display()
        else:
            if OnBoard(self.AdjustedMouse):
                piece = self.board.grid[self.AdjustedMouse.x][self.AdjustedMouse.y]
                if self.selectedPiece == piece:
                    self.draggedPiece = piece
                else:
                    self.SelectPiece(piece)

    def getMousePosition(self):
        x, y = pygame.mouse.get_pos()
        x = (x - Config.horizontal_offset) // Config.spotSize
        y = (y - Config.top_offset//2) // Config.spotSize
        self.AdjustedMouse = Position(x, y)


    def ReleasePiece(self):
        self.selectedPiece = None
        self.selectedPieceMoves = None
        self.selectedPieceCaptures = None
        self.draggedPiece = None
        self.selectedOrigin = None


    def Render(self):
        self.DrawChessBoard()
        if self.animateSpot >= Config.spotSize:
            self.DrawPieces()
        self.DrawHighlight()
        self.drawMoveLog()
        self.savegame()
        self.resign()

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
        # draw previous position
        nPosition, oldPosition = self.board.RecentMovePositions()
        if oldPosition and nPosition:
            x1 = oldPosition.x * Config.spotSize + Config.horizontal_offset
            y1 = oldPosition.y * Config.spotSize + Config.top_offset // 2 + 25
            x2 = nPosition.x * Config.spotSize + Config.horizontal_offset
            y2 = nPosition.y * Config.spotSize + Config.top_offset // 2 + 25
            pygame.draw.rect(self.screen,  (255, 255, 144), [x1, y1, Config.spotSize, Config.spotSize])
            pygame.draw.rect(self.screen,(252, 252, 179), [x2, y2, Config.spotSize, Config.spotSize])
        # Loop through the board grid and draw each piece on the screen
        for x in range(Config.boardSize):
            for y in range(Config.boardSize):
                x_pos = x * Config.spotSize + Config.horizontal_offset
                y_pos = y * Config.spotSize + Config.top_offset

                piece = self.board.grid[x][y]
                if piece is not None:
                    sprite = GetSprite(piece)
                    self.screen.blit(sprite, (x_pos, y_pos))
                elif self.board.grid[x][y] is not None:
                    y_pos += Config.spotSize // 2  # Adjust y_pos only if there is no piece
                    self.screen.blit(self.board.grid[x][y].sprite, (x_pos, y_pos))


    def RenderPromoteWindow(self):
        if self.board.pieceToPromote:
            if self.board.pieceToPromote.color == 0:
                x = self.board.pieceToPromote.position.x * Config.spotSize + Config.horizontal_offset
                y = self.board.pieceToPromote.position.y * Config.spotSize + Config.top_offset // 2 + 25
                pygame.draw.rect(self.screen, (200, 200, 200), [x, y, Config.spotSize , Config.spotSize * 4])
                for i in range(4):
                    piece = self.board.whitePromotions[i]
                    self.screen.blit(piece.sprite, (x, i * Config.spotSize + Config.top_offset //2 + 20 ))
                    bottomY = i * Config.spotSize + 50
                    pygame.draw.rect(self.screen, (0, 0, 0), [x, bottomY, Config.spotSize , 2])
            else:
                x = self.board.pieceToPromote.position.x * Config.spotSize + Config.horizontal_offset
                y = (self.board.pieceToPromote.position.y - 3) * Config.spotSize + Config.top_offset // 2 + 25
                pygame.draw.rect(self.screen, (200, 200, 200), [x, y, Config.spotSize , Config.spotSize * 4])
                for i in range(4):
                    piece = self.board.blackPromotions[i]
                    self.screen.blit(piece.sprite, (x, (i+4) * Config.spotSize + Config.top_offset //2 + 20 ))
                    bottomY = (i + 4) * Config.spotSize - 1 + 50
                    pygame.draw.rect(self.screen, (0, 0, 0), [x, bottomY, Config.spotSize , 2])

    # for the highlight of the pieces legal moves in the board and captures
    def DrawHighlight(self):
        # highlight selected piece
        if self.selectedPiece != None:
            x = self.selectedPiece.position.x * Config.spotSize + Config.horizontal_offset
            y = self.selectedPiece.position.y * Config.spotSize + Config.top_offset // 2 + 25
            pygame.draw.rect(self.screen, (190, 200, 222), [x, y, Config.spotSize, Config.spotSize])
            # self.screen.blit(oh, (x, y))
            if self.draggedPiece == None:
                self.screen.blit(self.selectedPiece.sprite, (x, y))

        # draw selectedPiece possible moves
        if self.selectedPiece and self.selectedPieceMoves:
            for move in self.selectedPieceMoves:
                x = move.x * Config.spotSize + Config.horizontal_offset
                y = move.y * Config.spotSize + Config.top_offset // 2 + 25
                self.screen.blit(ch, (x + 25 , y + 25 , Config.spotSize, Config.spotSize))
                # pygame.draw.rect(self.screen, (40, 130, 210), [x, y, Config.spotSize, Config.spotSize], Config.highlightOutline)

        # draw selected piece possible captures
        if self.selectedPiece and self.selectedPieceCaptures:
            for capturing in self.selectedPieceCaptures:
                x = capturing.x * Config.spotSize + Config.horizontal_offset
                y = capturing.y * Config.spotSize + Config.top_offset // 2 + 25
                self.screen.blit(rh, (x - 10, y - 10))

                # pygame.draw.rect(self.screen, (210, 211, 190), [x, y, Config.spotSize, Config.spotSize], Config.highlightOutline)

        # draw dragged piece
        if self.draggedPiece is not None:
            x = self.AdjustedMouse.x * Config.spotSize + Config.horizontal_offset
            y = self.AdjustedMouse.y * Config.spotSize + Config.top_offset // 2 + 25

            # Scale the sprite for dragged piece with SRCALPHA to improve quality
            original_sprite = self.draggedPiece.sprite.convert_alpha()
            scaled_sprite = pygame.transform.smoothscale(original_sprite, (int(Config.spotSize * 1.2), int(Config.spotSize * 1.2)))
            scaled_x = x - (scaled_sprite.get_width() - Config.spotSize) // 2
            scaled_y = y - (scaled_sprite.get_height() - Config.spotSize) // 2

            self.screen.blit(scaled_sprite, (scaled_x, scaled_y))


        # highlight if in Check
        # white king in check
        if self.board.checkWhiteKing:
            x = self.board.WhiteKing.position.x * Config.spotSize + Config.horizontal_offset
            y = self.board.WhiteKing.position.y * Config.spotSize + Config.top_offset // 2 + 25
            pygame.draw.rect(self.screen, (240, 111, 150), [x, y, Config.spotSize, Config.spotSize])
            self.screen.blit(self.board.WhiteKing.sprite, (x, y))
        # black king in check
        elif self.board.checkBlackKing:
            x = self.board.BlackKing.position.x * Config.spotSize + Config.horizontal_offset
            y = self.board.BlackKing.position.y * Config.spotSize + Config.top_offset // 2 + 25
            pygame.draw.rect(self.screen, (240, 111, 150), [x, y, Config.spotSize, Config.spotSize])
            self.screen.blit(self.board.BlackKing.sprite, (x, y))

        if self.animateSpot >= Config.spotSize:
            self.DrawChessCoordinate()

        self.RenderPromoteWindow()


    def drawMoveLog(self):
        logX = Config.board_display_size + Config.horizontal_offset + 20
        logY = Config.top_offset
        logWidth = Config.resolution[0] - logX - 50
        moveTexts = self.board.moveLog
        movesPerRow = 6
        corner_radius = 10

        logRect = pygame.Rect(logX, logY, logWidth, 500)
        pygame.draw.rect(self.screen, (204, 204, 204), logRect, border_radius=corner_radius)

        for i, moveText in enumerate(moveTexts):
            moveTextSurface = self.moveLogFont.render(moveText, True, (0, 0, 0))
            moveX = logX + (i % movesPerRow) * (logWidth // movesPerRow)
            moveY = logY + (i // movesPerRow) * 20
            self.screen.blit(moveTextSurface, (moveX, moveY))


    def savegame(self):
        logX = Config.board_display_size + Config.horizontal_offset + 80
        logY = Config.top_offset + 650
        logWidth = Config.resolution[0] - logX - 150
        button_height = 50
        button_text = "Save Game"
        save_button = Button(self.screen, logX + logWidth // 2, logY + button_height // 2, logWidth, button_height, button_text)
        save_button.Draw()

    def resign(self):
        logX = Config.board_display_size + Config.horizontal_offset + 80
        logY = Config.top_offset + 750
        logWidth = Config.resolution[0] - logX - 150
        button_height = 50
        button_text = "Resign"
        save_button = Button(self.screen, logX + logWidth // 2, logY + button_height // 2, logWidth, button_height, button_text)
        save_button.Draw()

