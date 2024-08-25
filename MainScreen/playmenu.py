import pygame
import ui
from setting import Config,sounds
from MainScreen.chess import Chess
from MainScreen.fadeeffect import fade_out,fade_in
from MainScreen.menu import Menu

class PlayMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg2blur.png")
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
        self.chess = Chess(screen)

    def DrawButtons(self):
        self.vs_player.Draw()
        self.vs_bot.Draw()
        self.back.Draw()

    def HandleClick(self,screen):
        mouse_position = pygame.mouse.get_pos()
        if self.vs_player.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            fade_in(screen)
            return 'Vsplayer'
        elif self.vs_bot.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            fade_in(screen)
            return 'bots'

        elif self.back.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            return 'main'

    def draw_username(self):
        if Menu.is_logged_in and Menu.logged_in_user:
            font = pygame.font.Font('assets/font/KnightWarrior-w16n8.ttf', 32)
            text_surface = font.render(f"Player : {Menu.logged_in_user}", True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.topright = (Config.width - 40, 30)
            self.screen.blit(text_surface, text_rect)

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
            self.draw_username()
            pygame.display.update()
