import pygame
import ui
from setting import Config,sounds
from MainScreen.fadeeffect import fade_out,fade_in
from MainScreen.menu import Menu

class OptionMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg2.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)

        # for logo
        self.title_image = pygame.image.load("./assets/images/logo (1).png")
        self.title_image = pygame.transform.smoothscale(self.title_image, (Config.width // 2.5, Config.height // 1.6))
        self.title_image_rect = self.title_image.get_rect(center=(Config.width // 2, Config.height // 4))

        button_y_start = Config.height // 2 -20
        button_spacing = 110
        self.option1 = ui.Button(screen, Config.width // 2, button_y_start, 300, 80, "Leaderboard")
        self.option2 = ui.Button(screen, Config.width // 2, button_y_start + button_spacing, 300, 80, "Rules")
        self.back = ui.Button(screen, Config.width // 2, button_y_start + 2 * button_spacing, 300, 80, "Back")

        self.running = True
        self.clock = pygame.time.Clock()

    def DrawButtons(self):
        self.option1.Draw()
        self.option2.Draw()
        self.back.Draw()

    def draw_username(self):
        if Menu.is_logged_in and Menu.logged_in_user:
            font = pygame.font.Font('assets/font/KnightWarrior-w16n8.ttf', 32)
            text_surface = font.render(f"Player : {Menu.logged_in_user}", True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.topright = (Config.width - 40, 30)
            self.screen.blit(text_surface, text_rect)

    def HandleClick(self,screen):
        mouse_position = pygame.mouse.get_pos()
        if self.option1.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            fade_in(screen)
            return'leaderboard'

        if self.option2.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            fade_in(screen)
            return'rule'

        elif self.back.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            return 'main'

    def Run(self):
        while self.running:
            self.clock.tick(Config.fps)
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
            self.screen.blit(self.title_image, self.title_image_rect.topleft)
            self.DrawButtons()
            self.draw_username()
            pygame.display.update()
