import pygame
import sys
import time
import json
import os

from setting import Config, sounds
from tools import Position, OnBoard
from utils import GetSprite, bh, oh, ch ,rh
from board import Board
import ui
from AI.ChessAI import Minimax

class Chess:
    def __init__(self, screen, ai_depth=1, time_control=None):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.gameOver = False
        self.animateSpot = 5
        self.selectedPiece = None
        self.selectedPieceMoves = None
        self.selectedPieceCaptures = None
        self.draggedPiece = None
        self.CanBeReleased = False
        self.AdjustedMouse = Position(0, 0)
        self.gameOverBackground = pygame.image.load("./assets/images/mainbg2blur.png")
        self.gameOverBackground = pygame.transform.smoothscale(self.gameOverBackground, Config.resolution)
        self.gameOverHeader = ui.TextUI(self.screen, "GAME OVER", Config.width//2, Config.height//6, 80, (255, 255, 255))
        self.gameOverHeader.centered = True
        self.winnerText = ui.TextUI(self.screen, "White Won the game", Config.width//2, Config.height//2, 180, (190, 255, 180))
        self.winnerText.centered = True
        self.background = pygame.image.load("./assets/images/mainbg2blur.png")
        self.background = pygame.transform.scale(self.background, Config.resolution)
        self.moveLogFont = pygame.font.SysFont("Verdana", 18)
        self.ComputerAI = Minimax(ai_depth, self.board, True, True)
        self.player_turn = 0
        self.current_save_slot = 1
        self.placeholder_player_turn = self.player_turn

        # for button
        button_y_start = Config.height // 2 - 60
        button_spacing = 110
        self.Save = ui.Button(screen, Config.width // 2 + 580, button_y_start + 3 * button_spacing, 200, 60, "Save Game")
        self.Resign = ui.Button(screen, Config.width // 2 + 580, button_y_start + 3.8 * button_spacing, 200, 60, "Resign Game")

        # for time display and management
        self.time_control = time_control
        self.white_time = 0
        self.black_time = 0
        self.last_move_time = 0

        if time_control:
            self.white_time = time_control['initial'] * 60  # to convert to seconds
            self.black_time = time_control['initial'] * 60




    def GetFrameRate(self):
        return self.clock.get_fps()

    def vsComputer(self):
        pygame.event.clear()
        sounds.game_start_sound.play()
        while not self.gameOver:
            self.clock.tick(Config.fps)
            self.background = pygame.image.load("./assets/images/mainbg2blur.png")
            self.getMousePosition()
            # update window caption
            pygame.display.set_caption("Chess : VS Computer " + str(int(self.GetFrameRate())))
            self.display()
            self.ComputerMoves(1)
            if self.gameOver == False:
                if self.animateSpot >= Config.spotSize:
                    self.HandleEvents()
                    self.IsGameOver()

    def vsPlayer(self):
        pygame.event.clear()
        sounds.game_start_sound.play()
        self.last_move_time = time.time()
        while not self.gameOver:
            self.clock.tick(Config.fps)
            self.background = pygame.image.load("./assets/images/mainbg2blur.png")
            self.getMousePosition()
            pygame.display.set_caption("Chess : VS Player " + str(int(self.GetFrameRate())))
            if self.time_control:
                self.update_time()
            self.display()
            if self.animateSpot >= Config.spotSize:
                self.HandleEvents()
            self.IsGameOver()
            if self.check_time_out():
                self.IsGameOver()

    def set_ai_depth(self, depth):
        self.ComputerAI = Minimax(depth, self.board, True, True)

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
                    self.HandleOnLeftMouseButtonDown(event)
                elif event.button == 3:
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.HandleOnLeftMouseButtonUp()


    def ComputerMoves(self, player):
        if self.board.player == player:
            piece, bestmove = self.ComputerAI.Start(0)
            self.board.Move(piece, bestmove)
            if self.board.pieceToPromote is not None:
                self.board.PromotePawn(self.board.pieceToPromote, 0)

            if bestmove:
                if self.board.GetPiece(bestmove) is not None:
                    sounds.move_sound.play()
                else:
                    self.move_sound.play()


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



    def HandleOnLeftMouseButtonDown(self,event):
        mouse_position = pygame.mouse.get_pos()
        if self.Resign.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            self.board.Forfeit()
        if self.Save.get_rect().collidepoint(event.pos):
            sounds.button_sound.play()
            self.save_game()
            # return 'main'
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

    def IsGameOver(self):
        if self.board.winner != None:
            self.gameOver = True
            # print("the game is over")
            self.display()
            self.gameOverWindow()

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
        self.drawCapturedPieces()
        self.Save.Draw()
        self.Resign.Draw()
        self.drawTimer()

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


    def drawCapturedPieces(self):
        # Define rectangle dimensions and positions
        rect_width = 300
        rect_height = 200
        left_margin = 60
        top_margin = Config.top_offset
        bottom_margin = Config.top_offset + Config.board_display_size - rect_height

        # Draw rectangles
        pygame.draw.rect(self.screen, (204, 204, 204), [left_margin, top_margin, rect_width, rect_height], border_radius=10)
        pygame.draw.rect(self.screen, (204, 204, 204), [left_margin, bottom_margin, rect_width, rect_height], border_radius=10)

        # Draw captured pieces
        piece_size = 50
        pieces_per_row = rect_width // piece_size

        # Draw white captured pieces (top rectangle)
        for i, piece in enumerate(self.board.captured_white_pieces):
            x = left_margin + (i % pieces_per_row) * piece_size
            y = top_margin + (i // pieces_per_row) * piece_size
            sprite = pygame.transform.scale(GetSprite(piece), (piece_size, piece_size))
            self.screen.blit(sprite, (x, y))

        # Draw black captured pieces (bottom rectangle)
        for i, piece in enumerate(self.board.captured_black_pieces):
            x = left_margin + (i % pieces_per_row) * piece_size
            y = bottom_margin + (i // pieces_per_row) * piece_size
            sprite = pygame.transform.scale(GetSprite(piece), (piece_size, piece_size))
            self.screen.blit(sprite, (x, y))

    # def save_game(self):
    #     game_state = {
    #         "player_turn": self.board.player,
    #         "board_state": [[(piece.code, piece.color) if piece else None for piece in row] for row in self.board.grid]
    #     }

    #     save_slot = f"save_slot_{self.current_save_slot}.json"
    #     save_path = os.path.join("Saved_Games", save_slot)

    #     with open(save_path, 'w') as f:
    #         json.dump(game_state, f)

    #     self.current_save_slot = (self.current_save_slot % 3) + 1

    def save_game(self):
        game_state = {
            "player_turn": self.board.player,
            "board_state": [[(piece.code, piece.color) if piece else None for piece in row] for row in self.board.grid]
        }

        # Find the next available save slot
        for slot in range(1, 4):  # for 3 slots
            save_slot = f"save_slot_{slot}.json"
            save_path = os.path.join("Saved_Games", save_slot)

            if not os.path.exists(save_path):
                # If this slot doesn't exist, use it
                with open(save_path, 'w') as f:
                    json.dump(game_state, f)
                print(f"Game saved in slot {slot}")
                return

        # If all slots are used, overwrite the oldest one (slot 1)
        save_slot = "save_slot_1.json"
        save_path = os.path.join("Saved_Games", save_slot)
        with open(save_path, 'w') as f:
            json.dump(game_state, f)
        print("All save slots were full. Overwrote save slot 1.")


    def update_time(self):
        if self.time_control:
            current_time = time.time()
            if self.last_move_time:
                elapsed = current_time - self.last_move_time
                if self.board.player == 0:  # White's turn
                    self.white_time -= elapsed
                else:
                    self.black_time -= elapsed
            self.last_move_time = current_time

    def check_time_out(self):
        if self.time_control:
            if self.white_time <= 0:
                self.board.winner = 1  # Black wins
                return True
            elif self.black_time <= 0:
                self.board.winner = 0  # White wins
                return True
        return False

    def drawTimer(self):
        if self.time_control:
            white_time_str = time.strftime("%M:%S", time.gmtime(max(0, self.white_time)))
            black_time_str = time.strftime("%M:%S", time.gmtime(max(0, self.black_time)))

            font = pygame.font.Font('assets/font/Roboto-Bold.ttf', 38)  # Font size

            # Render timer texts
            black_timer = font.render(f"{black_time_str}", True,  (255, 255, 255))
            white_timer = font.render(f"{white_time_str}", True, (0, 0, 0))

            # Get the width and height of the timer text to size the rectangles perfectly
            black_timer_rect = black_timer.get_rect()
            white_timer_rect = white_timer.get_rect()

            # Position the timers on the screen
            timer_x = 80  # Horizontal position
            black_timer_y = Config.height // 3
            white_timer_y = (Config.height * 2) // 3


            padding = 10
            black_rect_width = black_timer_rect.width + 20 + padding * 2
            black_rect_height = black_timer_rect.height + padding * 2

            white_rect_width = white_timer_rect.width + 20 + padding * 2
            white_rect_height = white_timer_rect.height + padding * 2

            # Draw background rectangles for better visibility
            pygame.draw.rect(self.screen, (0, 0, 0),
                            (timer_x - padding, black_timer_y - black_rect_height // 2,
                            black_rect_width + 15, black_rect_height), border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255),
                            (timer_x - padding, white_timer_y - white_rect_height // 2,
                            white_rect_width + 15, white_rect_height), border_radius=10)

            # Center the timer text within the rectangles
            black_timer_center = (timer_x + black_rect_width // 2 - black_timer_rect.width // 2,
                                black_timer_y - black_timer_rect.height // 2)
            white_timer_center = (timer_x + white_rect_width // 2 - white_timer_rect.width // 2,
                                white_timer_y - white_timer_rect.height // 2)

            # Blit timers to the screen
            self.screen.blit(black_timer, black_timer_center)
            self.screen.blit(white_timer, white_timer_center)


    def gameOverWindow(self):
        if self.board.winner >= 0:
            sounds.checkmatewin_sound.play()
        else:
            sounds.checkmatelose_sound.play()
        time.sleep(3)
        self.screen.blit(self.gameOverBackground, (0, 0))
        self.gameOverHeader.Draw()
        if self.board.winner  == 0:
            self.winnerText.text = "White Won"

            king_image = self.board.WhiteKing.sprite
            scaled_king_image = pygame.transform.scale(king_image, (king_image.get_width() + 20, king_image.get_height() + 20))
            self.screen.blit(scaled_king_image, (Config.width // 2 - Config.spotSize // 2, Config.height // 3 - 50))

        elif self.board.winner == 1:
            self.winnerText.text = "Black Won"
            king_image = self.board.BlackKing.sprite
            scaled_king_image = pygame.transform.scale(king_image, (king_image.get_width() + 20, king_image.get_height() + 20))
            self.screen.blit(scaled_king_image, (Config.width // 2 - Config.spotSize // 2, Config.height // 3 - 50))
        else:
            self.winnerText.text = "StaleMate"

        self.gameOverHeader.Draw()
        self.winnerText.Draw()
        pygame.display.update()
        time.sleep(5)
        self.board = Board()
        self.animateSpot = 1
