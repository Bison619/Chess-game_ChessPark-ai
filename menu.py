import pygame
from setting import Config

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)
        # for logo
        self.title_image = pygame.image.load("./assets/images/logo (1).png")
        self.title_image = pygame.transform.smoothscale(self.title_image, (Config.width // 2.5, Config.height // 1.6))
        self.title_image_rect = self.title_image.get_rect(center=(Config.width // 2, Config.height // 4))
        self.running = True
        self.clock = pygame.time.Clock()

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

            # display background image
            self.screen.blit(self.background, (0, 0))
            # for logo
            self.screen.blit(self.title_image, self.title_image_rect.topleft)
            # update screen
            pygame.display.update()