import pygame
from setting import Config, sounds
from MainScreen.fadeeffect import fade_out
from ui import TextUI, Text2UI
import ui

class BotsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg2blur.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)
        self.header_text = TextUI(screen, "Bots", Config.width // 2 - 70, 30, 72, (255, 255, 255))
        self.subheader_beginner = TextUI(screen, "Beginner", Config.width // 2 - 60, 140, 32, (0, 255, 0))
        self.subheader_intermediate = TextUI(screen, "Intermediate", Config.width // 2 - 70, 400, 32, (255, 255, 0))
        self.subheader_expert = TextUI(screen, "Expert", Config.width // 2 - 70, 660, 32, (255, 0, 0))
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
            pygame.image.load("./assets/images/bot1.png"),
            pygame.image.load("./assets/images/bot1.png"),
            pygame.image.load("./assets/images/bot1.png"),
            pygame.image.load("./assets/images/bot1.png"),
            pygame.image.load("./assets/images/bot1.png"),
            pygame.image.load("./assets/images/bot1.png")
        ]
        self.images = [pygame.transform.scale(image, (box_width, box_height)) for image in self.images]

        # Text below boxes of the player and elo
        self.bot_texts = [
            Text2UI(screen, "Name: Max\nELO: 100", self.box_positions[0][0], self.box_positions[0][1] + 140, 16, (0, 255, 0)),
            Text2UI(screen, "Name: Alice\nELO: 120", self.box_positions[1][0], self.box_positions[1][1] + 140, 16, (0, 255, 0)),
            Text2UI(screen, "Name: Bob\nELO: 90", self.box_positions[2][0], self.box_positions[2][1] + 140, 16, (0, 255, 0)),
            Text2UI(screen, "Name: Charlie\nELO: 150", self.box_positions[3][0], self.box_positions[3][1] + 140, 16, (255, 255, 0)),
            Text2UI(screen, "Name: Emily\nELO: 110", self.box_positions[4][0], self.box_positions[4][1] + 140, 16, (255, 255, 0)),
            Text2UI(screen, "Name: Jack\nELO: 95", self.box_positions[5][0], self.box_positions[5][1] + 140, 16, (255, 0, 0))
        ]

        button_y_start = Config.height // 2 - 20
        button_spacing = 110
        self.back_button = ui.Button(screen, Config.width // 2 + 600, button_y_start + 3.6 * button_spacing, 200, 60, "Back")

        self.running = True
        self.clock = pygame.time.Clock()

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

    def HandleClick(self, screen):
        mouse_position = pygame.mouse.get_pos()
        if self.back_button.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            return 'play'

    def Run(self):
        while self.running:
            self.clock.tick(Config.fps)
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

            self.DrawButtons()
            pygame.display.update()
