import pygame, os
import ui
import requests
from setting import Config,sounds
from MainScreen.chess import Chess
from MainScreen.fadeeffect import fade_in,fade_out
from MainScreen.login_screen import LoginScreen
from MainScreen.background import Background

# for back-ground music
pygame.mixer.music.load(os.path.join('assets/sounds/bg space music.mp3'))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg2.png")
        self.backgroundblur = pygame.image.load("./assets/images/mainbg2blur.png")
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
        self.log_button = ui.Button(screen, Config.width // 2 + 640, button_y_start + 3 * button_spacing, 60, 60, "Log In")
        self.register_button = ui.Button(screen, Config.width // 2 + 640, button_y_start + 3.7 * button_spacing, 120, 60, "Register")
        self.logout_button = ui.Button(screen, Config.width // 2 - 640, button_y_start + 3.7 * button_spacing, 120, 60, "Logout")

        self.running = True
        self.clock = pygame.time.Clock()
        self.chess = Chess(screen)
        self.sakura_background = Background(screen)
        self.login_screen = None
        self.register_screen = None
        self.logged_in_user = None
        self.is_logged_in = False
        self.font = pygame.font.Font('assets/font/KnightWarrior-w16n8.ttf', 32)

    def DrawButtons(self):
        self.Play.Draw()
        self.Option.Draw()
        self.exit.Draw()
        self.load.Draw()
        if not self.is_logged_in:
            self.log_button.Draw()
            self.register_button.Draw()
        if  self.is_logged_in:
            self.logout_button.Draw()

    def register_user(self, username, password, email):
        url = "http://localhost:8000/authentication/register/"
        data = {
            "username": username,
            "password": password,
            "email": email
        }
        try:
            response = requests.post(url, json=data)
            self.show_register_message()
            return response.json()
        except requests.RequestException:
            self.show_loginerror_message()
            return {"status": "error", "message": "Network error"}

    def login_user(self, username, password):
        url = "http://localhost:8000/authentication/login/"
        data = {
            "username": username,
            "password": password
        }
        try:
            response = requests.post(url, json=data)
            result = response.json()
            if result['status'] == 'success':
                self.logged_in_user = username
                self.is_logged_in = True
                self.show_login_message()
            return result
        except requests.RequestException:
            self.show_loginerror_message()
            return {"status": "error", "message": "Network error"}

    def draw_username(self):
        if self.is_logged_in and self.logged_in_user:
            text_surface = self.font.render(f"Player : {self.logged_in_user}", True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.topright = (Config.width - 40, 30)
            self.screen.blit(text_surface, text_rect)
            self.logout_button.Draw()

    def logout(self):
        self.logged_in_user = None
        self.is_logged_in = False

    def show_login_message(self):
        self.screen.blit(self.backgroundblur, (0, 0))
        message = "You are Logged In..!! "
        font = pygame.font.Font('assets/font/KnightWarrior-w16n8.ttf', 64)
        text = font.render(message, True, (0, 255, 0))
        text_rect = text.get_rect(center=(Config.width // 2, Config.height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)

    def show_loginerror_message(self):
        self.screen.blit(self.backgroundblur, (0, 0))
        message = "Unexpected Error Try again..!! "
        font = pygame.font.Font('assets/font/KnightWarrior-w16n8.ttf', 64)
        text = font.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(Config.width // 2, Config.height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)

    def show_register_message(self):
        self.screen.blit(self.backgroundblur, (0, 0))
        message = "You are Registerd ..!! "
        font = pygame.font.Font('assets/font/KnightWarrior-w16n8.ttf', 64)
        text = font.render(message, True, (0, 255, 0))
        text_rect = text.get_rect(center=(Config.width // 2, Config.height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)

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
            fade_out(screen)
            self.login_screen = LoginScreen(screen)
            fade_in(screen)
            return 'login'

        elif self.register_button.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            self.register_screen = LoginScreen(screen, is_register=True)
            fade_in(screen)
            return 'register'

        elif self.is_logged_in and self.logout_button.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            self.logout()
            return 'main'

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
                            if next_screen == 'login':
                                self.login_screen = LoginScreen(self.screen)
                            elif next_screen == 'register':
                                self.register_screen = LoginScreen(self.screen, is_register=True)
                            else:
                                return next_screen

            # Handle login screen
            if self.login_screen:
                result = self.login_screen.run()
                if result:
                    if result != 'cancel':
                        if len(result) == 2:
                            username, password = result
                            login_result = self.login_user(username, password)
                            print(login_result['message'])
                        else:
                            print("Unexpected result from login screen")
                    self.login_screen = None

            # Handle register screen
            if self.register_screen:
                result = self.register_screen.run()
                if result:
                    if result != 'cancel':
                        if len(result) == 3:
                            username, password, email = result
                            register_result = self.register_user(username, password, email)
                            print(register_result['message'])
                        else:
                            print("Unexpected result from register screen")
                    self.register_screen = None

            # display background image
            self.screen.blit(self.background, (0, 0))

            # for logo
            self.sakura_background.draw()
            self.screen.blit(self.title_image, self.title_image_rect.topleft)

            # Draw buttons
            self.draw_username()
            self.DrawButtons()

            # update screen
            pygame.display.update()