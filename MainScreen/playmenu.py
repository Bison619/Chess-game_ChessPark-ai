import pygame
import ui
from setting import Config

class PlayMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg2.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)

        # for logo
        self.title_image = pygame.image.load("./assets/images/logo (1).png")
        self.title_image = pygame.transform.smoothscale(self.title_image, (Config.width // 2.5, Config.height // 1.6))
        self.title_image_rect = self.title_image.get_rect(center=(Config.width // 2, Config.height // 4))

        button_y_start = Config.height // 2 - 20
        button_spacing = 110
        self.vs_player = ui.Button(screen, Config.width // 2, button_y_start, 300, 80, "Vs Player")
        self.vs_bot = ui.Button(screen, Config.width // 2, button_y_start + button_spacing, 300, 80, "Vs Bot")
        self.back = ui.Button(screen, Config.width // 2, button_y_start + 2 * button_spacing, 300, 80, "Back")

        self.running = True
        self.clock = pygame.time.Clock()

    def DrawButtons(self):
        self.vs_player.Draw()
        self.vs_bot.Draw()
        self.back.Draw()

    def HandleClick(self):
        mouse_position = pygame.mouse.get_pos()
        if self.vs_player.get_rect().collidepoint(mouse_position):
            pass
        elif self.vs_bot.get_rect().collidepoint(mouse_position):
            pass
        elif self.back.get_rect().collidepoint(mouse_position):
            return 'main'

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
                    next_screen = self.HandleClick()
                    if next_screen:
                        return next_screen

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.title_image, self.title_image_rect.topleft)
            self.DrawButtons()
            pygame.display.update()
