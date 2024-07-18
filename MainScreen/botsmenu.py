import pygame
from setting import Config, sounds
from MainScreen.fadeeffect import fade_out
from ui import TextUI
import ui

class BotsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg2blur.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)

        # Initialize TextUI instances for headers and text below boxes
        self.header_text = TextUI(screen, "Bots", Config.width // 2, 30, 48, (255, 255, 255))  # Larger header
        self.subheader_beginner = TextUI(screen, "Beginner", Config.width // 2, 100, 24, (200, 200, 200))
        self.subheader_intermediate = TextUI(screen, "Intermediate", Config.width // 2, 310, 24, (200, 200, 200))
        self.subheader_expert = TextUI(screen, "Expert", Config.width // 2, 520, 24, (200, 200, 200))

        # Boxes with images positions (centered horizontally)
        box_width = 150
        box_height = 150
        box_spacing = 50
        box_x_start = (Config.width - (3 * box_width + 2 * box_spacing)) // 2  # Centered position
        self.box_positions = [
            (box_x_start, 200),
            (box_x_start + box_width + box_spacing, 200),
            (box_x_start + 2 * (box_width + box_spacing), 200),
            (box_x_start, 410),
            (box_x_start + box_width + box_spacing, 410),
            (box_x_start + 2 * (box_width + box_spacing), 410)
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

        # Scale images to fit the box size (optional)
        self.images = [pygame.transform.scale(image, (box_width, box_height)) for image in self.images]

        # Text below boxes
        self.bot_texts = [
            TextUI(screen, "Name: Max\nELO: 100", self.box_positions[0][0], self.box_positions[0][1] + 160, 20, (255, 255, 255)),
            TextUI(screen, "Name: Alice\nELO: 120", self.box_positions[1][0], self.box_positions[1][1] + 160, 20, (255, 255, 255)),
            TextUI(screen, "Name: Bob\nELO: 90", self.box_positions[2][0], self.box_positions[2][1] + 160, 20, (255, 255, 255)),
            TextUI(screen, "Name: Charlie\nELO: 150", self.box_positions[3][0], self.box_positions[3][1] + 160, 20, (255, 255, 255)),
            TextUI(screen, "Name: Emily\nELO: 110", self.box_positions[4][0], self.box_positions[4][1] + 160, 20, (255, 255, 255)),
            TextUI(screen, "Name: Jack\nELO: 95", self.box_positions[5][0], self.box_positions[5][1] + 160, 20, (255, 255, 255))
        ]

        # Buttons
        button_y_start = Config.height // 2 - 20
        button_spacing = 110
        self.back_button = ui.Button(screen, Config.width // 2, button_y_start + 3 *button_spacing, 300, 80, "Back")

        self.running = True
        self.clock = pygame.time.Clock()

    def DrawButtons(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))

        # Draw headers and subheaders using TextUI
        self.header_text.Draw()
        self.subheader_beginner.Draw()
        self.subheader_intermediate.Draw()
        self.subheader_expert.Draw()

        # Draw boxes with images and text
        for i, (x, y) in enumerate(self.box_positions):
            pygame.draw.rect(self.screen, (100, 100, 100), (x, y, 150, 150))
            self.screen.blit(self.images[i], (x, y))  # Draw image inside the box
            self.bot_texts[i].Draw()  # Draw text below each box

        # Draw buttons
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


