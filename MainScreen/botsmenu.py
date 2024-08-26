import pygame
from setting import Config, sounds
from MainScreen.fadeeffect import fade_out
from ui import TextUI, Text2UI
from board import Board
import ui
from MainScreen.chess import Chess
from MainScreen.menu import Menu

class BotsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.background = pygame.image.load("./assets/images/mainbg2blur.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)
        self.header_text = TextUI(screen, "Bots", Config.width // 2 - 70, 30, 72, (255, 255, 255))
        self.subheader_beginner = TextUI(screen, "Beginner", Config.width // 2 - 60, 140, 32, (0, 255, 0))
        self.subheader_intermediate = TextUI(screen, "Intermediate", Config.width // 2 - 70, 400, 32, (255, 255, 0))
        self.subheader_expert = TextUI(screen, "Expert", Config.width // 2 - 70, 660, 32, (255, 0, 0))
        self.clock = pygame.time.Clock()

        box_width = 130
        box_height = 130
        box_spacing = 60
        box_x_start = (Config.width - (3 * box_width + 2 * box_spacing)) // 2
        self.box_positions = [
            (box_x_start, 200),
            (box_x_start + box_width + box_spacing, 200),
            (box_x_start + 2 * (box_width + box_spacing), 200),
            (box_x_start, 460),
            (box_x_start + box_width + box_spacing, 460),
            (box_x_start, 700)
        ]

        # Load images for each box
        self.images = [
            pygame.image.load("./assets/images/bbot1.png"),
            pygame.image.load("./assets/images/bbot2.png"),
            pygame.image.load("./assets/images/bbot3.png"),
            pygame.image.load("./assets/images/ibot1.png"),
            pygame.image.load("./assets/images/ibot2.png"),
            pygame.image.load("./assets/images/ebot1.png")
        ]
        self.images = [pygame.transform.scale(image, (box_width, box_height)) for image in self.images]

        # Text below boxes of the player and elo
        self.bot_texts = [
            Text2UI(screen, "Name: Max\nPoints: 600", self.box_positions[0][0], self.box_positions[0][1] + 140, 16, (0, 255, 0)),
            Text2UI(screen, "Name: Alice\nPoints: 700", self.box_positions[1][0], self.box_positions[1][1] + 140, 16, (0, 255, 0)),
            Text2UI(screen, "Name: Bob\nPoints: 800", self.box_positions[2][0], self.box_positions[2][1] + 140, 16, (0, 255, 0)),
            Text2UI(screen, "Name: Mark Rober\nPoints: 1000", self.box_positions[3][0], self.box_positions[3][1] + 140, 16, (255, 255, 0)),
            Text2UI(screen, "Name: GothamChess\nPoints: 1100", self.box_positions[4][0], self.box_positions[4][1] + 140, 16, (255, 255, 0)),
            Text2UI(screen, "Name: Magnus Carlson\nPoints: 1500", self.box_positions[5][0], self.box_positions[5][1] + 140, 16, (255, 0, 0))
        ]

        button_y_start = Config.height // 2 - 20
        button_spacing = 110
        self.back_button = ui.Button(screen, Config.width // 2 + 600, button_y_start + 3.6 * button_spacing, 200, 60, "Back")

        self.running = True
        self.clock = pygame.time.Clock()
        self.chess = None
        self.bot_points = [600, 700, 800, 1000, 1100, 1500]


    def DrawButtons(self):
        self.screen.blit(self.background, (0, 0))
        self.header_text.Draw()
        self.subheader_beginner.Draw()
        self.subheader_intermediate.Draw()
        self.subheader_expert.Draw()
        for i, (x, y) in enumerate(self.box_positions):
            pygame.draw.rect(self.screen, (100, 100, 100), (x, y, 130, 130))
            self.screen.blit(self.images[i], (x, y))
            self.bot_texts[i].Draw()
        self.back_button.Draw()

    def draw_username(self):
        if Menu.is_logged_in and Menu.logged_in_user:
            font = pygame.font.Font('assets/font/KnightWarrior-w16n8.ttf', 32)
            text_surface = font.render(f"Player : {Menu.logged_in_user}", True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.topright = (Config.width - 40, 30)
            self.screen.blit(text_surface, text_rect)

    def HandleClick(self, screen):
        mouse_position = pygame.mouse.get_pos()
        if self.back_button.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            return 'play'
        for i, (x, y) in enumerate(self.box_positions):
            if pygame.Rect(x, y, 130, 130).collidepoint(mouse_position):
                self.start_game(i)
                pygame.mixer.music.stop()
                self.screen.blit(self.background, (0, 0))

    def start_game(self, index):
        depth_mapping = {
            0: 1,  # Beginner 1
            1: 1,  # Beginner 2
            2: 2,  # Beginner 3
            3: 3,  # Intermediate 1
            4: 3,  # Intermediate 2
            5: 4   # Expert
        }
        depth = depth_mapping.get(index, 1)
        print(f"AI Depth: {depth}")
        self.chess = Chess(self.screen, ai_depth=depth, bot_points=self.bot_points[index])
    # Set the background to mainbg
        sounds.button_sound.play()
        self.chess.vsComputer()
        self.background = pygame.image.load("./assets/images/mainbg2blur.png")
        self.clock.tick(Config.fps)

    def Run(self):
        while self.running:
            self.clock.tick(Config.fps)
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        return 'main'
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    next_screen = self.HandleClick(self.screen)
                    if next_screen:
                        return next_screen

            self.screen.blit(self.background, (0, 0))
            self.DrawButtons()
            self.draw_username()
            pygame.display.update()

