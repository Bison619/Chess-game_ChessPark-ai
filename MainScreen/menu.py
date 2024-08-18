import pygame, os
import ui
from setting import Config,sounds
from MainScreen.chess import Chess
from MainScreen.fadeeffect import fade_in,fade_out
from MainScreen.login_screen import LoginScreen
import requests

# for back-ground music
pygame.mixer.music.load(os.path.join('assets/sounds/bg space music.mp3'))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg2.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)
        self.login_screen = None
        # for logo
        self.title_image = pygame.image.load("./assets/images/logo (1).png")
        self.title_image = pygame.transform.smoothscale(self.title_image, (Config.width // 2.5, Config.height // 1.6))
        self.title_image_rect = self.title_image.get_rect(center=(Config.width // 2, Config.height // 4))

        # for buttons
        button_y_start = Config.height // 2 - 20
        button_spacing = 110
        self.Play = ui.Button(screen, Config.width // 2, button_y_start, 200, 80, "New Game")
        self.load = ui.Button(screen, Config.width // 2, button_y_start +  button_spacing, 200, 80, "Load Game")
        self.Option = ui.Button(screen, Config.width // 2, button_y_start + 2 *  button_spacing, 200, 80, "Option")
        self.exit = ui.Button(screen, Config.width // 2, button_y_start + 3 * button_spacing, 200, 80, "Exit")
        self.log_button = ui.Button(screen, Config.width // 2 + 640, button_y_start + 3.7 * button_spacing, 120, 60, "Log In")

        self.running = True
        self.clock = pygame.time.Clock()
        self.chess = Chess(screen)

    def DrawButtons(self):
        self.Play.Draw()
        self.Option.Draw()
        self.exit.Draw()
        self.load.Draw()
        self.log_button.Draw()

    def HandleClick(self,screen):
        mouse_position = pygame.mouse.get_pos()
        if self.Play.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            fade_in(screen)
            return'play'
        elif self.load.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            fade_in(screen)
            return'load'
        elif self.Option.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            fade_in(screen)
            return'option'
        elif self.exit.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            self.running = False
            fade_out(screen)
        elif self.log_button.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            self.login_screen = LoginScreen(screen)
            return 'login'

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
                        next_screen = self.HandleClick(self.screen)
                        if next_screen:
                            return next_screen

            # display background image
            self.screen.blit(self.background, (0, 0))
            # for logo
            self.screen.blit(self.title_image, self.title_image_rect.topleft)
            self.DrawButtons()
            # update screen
            pygame.display.update()