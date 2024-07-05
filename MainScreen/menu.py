import pygame
import ui
from setting import Config
from MainScreen.chess import Chess


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg2.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)
        # for logo
        self.title_image = pygame.image.load("./assets/images/logo (1).png")
        self.title_image = pygame.transform.smoothscale(self.title_image, (Config.width // 2.5, Config.height // 1.6))
        self.title_image_rect = self.title_image.get_rect(center=(Config.width // 2, Config.height // 4))

        # for buttons
        button_y_start = Config.height // 2 - 20
        button_spacing = 110
        self.Play = ui.Button(screen, Config.width // 2, button_y_start, 200, 80, "Play")
        self.Option = ui.Button(screen, Config.width // 2, button_y_start + button_spacing, 200, 80, "Option")
        self.exit = ui.Button(screen, Config.width // 2, button_y_start + 2 * button_spacing, 200, 80, "Exit")

        self.running = True
        self.clock = pygame.time.Clock()
        self.chess = Chess(screen)

    def DrawButtons(self):
        self.Play.Draw()
        self.Option.Draw()
        self.exit.Draw()

    def HandleClick(self):
        mouse_position = pygame.mouse.get_pos()
        if self.Play.get_rect().collidepoint(mouse_position):
             return'play'
        elif self.Option.get_rect().collidepoint(mouse_position):
               return'option'
        elif self.exit.get_rect().collidepoint(mouse_position):
            self.running = False

    def GetFrameRate(self):
        return self.clock.get_fps()

    def Run(self):
        while self.running:
            self.clock.tick(Config.fps)
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    # left mouse click
                    if event.button == 1:
                        next_screen = self.HandleClick()
                        if next_screen:
                            return next_screen

            # display background image
            self.screen.blit(self.background, (0, 0))
            # for logo
            self.screen.blit(self.title_image, self.title_image_rect.topleft)
            self.DrawButtons()
            # update screen
            pygame.display.update()