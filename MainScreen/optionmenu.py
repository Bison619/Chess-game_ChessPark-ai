import pygame
import ui
from setting import Config

class OptionMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)

        button_y_start = Config.height // 2 - 20
        self.back = ui.Button(screen, Config.width // 2, button_y_start, 200, 80, "Back")

        self.running = True
        self.clock = pygame.time.Clock()

    def DrawButtons(self):
        self.back.Draw()

    def HandleClick(self):
        mouse_position = pygame.mouse.get_pos()
        if self.back.get_rect().collidepoint(mouse_position):
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
            self.DrawButtons()
            pygame.display.update()
