import pygame
import ui
import os
import json

from Fen import *
from utils import GetSprite
from setting import Config,sounds
from board import Board
from MainScreen.chess import Chess
from tools import Position
from MainScreen.fadeeffect import fade_out

class LoadMenu:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.background = pygame.image.load("./assets/images/mainbg2.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)

        # for logo
        self.title_image = pygame.image.load("./assets/images/logo (1).png")
        self.title_image = pygame.transform.smoothscale(self.title_image, (Config.width // 2.5, Config.height // 1.6))
        self.title_image_rect = self.title_image.get_rect(center=(Config.width // 2, Config.height // 4))

        button_y_start = Config.height // 2 - 20
        button_spacing = 110
        self.Save1 = ui.Button(screen, Config.width // 2, button_y_start, 300, 80, "Save Slot 1")
        self.Save2 = ui.Button(screen, Config.width // 2, button_y_start + button_spacing, 300, 80, "Save Slot 2")
        self.Save3 = ui.Button(screen, Config.width // 2, button_y_start + 2 * button_spacing, 300, 80, "Save Slot 3")
        self.back = ui.Button(screen, Config.width // 2, button_y_start + 3 * button_spacing, 300, 80, "Back")

        self.running = True
        self.clock = pygame.time.Clock()
        self.chess = Chess(screen)
        self.save_slots = [
            self.Save1,
            self.Save2,
            self.Save3
        ]

    def DrawButtons(self):
        self.Save1.Draw()
        self.Save2.Draw()
        self.Save3.Draw()
        self.back.Draw()

    def LoadGame(self, slot_number):
        save_slot = f"save_slot_{slot_number}.json"
        save_path = os.path.join("Saved_Games", save_slot)

        if os.path.exists(save_path):
            with open(save_path, 'r') as f:
                game_state = json.load(f)

            # Set the player turn
            loaded_player_turn = game_state["player_turn"]
            self.chess.board.player = loaded_player_turn

            # Clear the current board
            self.chess.board.grid = [[None for _ in range(8)] for _ in range(8)]

            # Load new state
            for y, row in enumerate(game_state["board_state"]):
                for x, piece_info in enumerate(row):
                    if piece_info:
                        piece_code, color = piece_info
                        piece = self.chess.board.get_piece_from_code(piece_code, color, Position(y, x))
                        piece.sprite = GetSprite(piece)
                        self.chess.board.grid[y][x] = piece

            self.chess.Render()
            self.chess.vsPlayer()


    def HandleClick(self, screen):
        mouse_position = pygame.mouse.get_pos()
        for i, button in enumerate(self.save_slots):
            if button.get_rect().collidepoint(mouse_position):
                sounds.button_sound.play()
                self.LoadGame(i + 1)
                return

        if self.back.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            return 'main'

    def GetFrameRate(self):
        return self.clock.get_fps()

    def Run(self):
        while self.running:
            self.clock.tick(Config.fps)
            # update caption and frame rate
            pygame.display.set_caption("Chess " + str(int(self.GetFrameRate())))
            # display background image
            self.screen.blit(self.background, (0, 0))
            # handle Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    next_screen = self.HandleClick(self.screen)
                    if next_screen:
                        return next_screen

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.title_image, self.title_image_rect.topleft)
            self.DrawButtons()
            pygame.display.update()
