import pygame
import ui
from setting import Config, sounds


class LoginScreen:
    def __init__(self, screen, is_register=False):
        self.screen = screen
        self.is_register = is_register
        self.background = pygame.image.load("./assets/images/mainbg2frame.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)

        # Adjust the positions to create more space between input boxes and buttons
        input_y_start = Config.height // 2 - 75
        input_spacing = 50

        self.username_input = ui.InputBox(screen, Config.width // 2 - 110, input_y_start, 250, 35, "")
        self.password_input = ui.InputBox(screen, Config.width // 2 - 110, input_y_start + input_spacing * 1.5, 250, 35, '', is_password=True)
        self.email_input = ui.InputBox(screen, Config.width // 2 - 110, input_y_start + 2 * input_spacing * 1.5, 250, 35, "") if is_register else None

        # Adjust button positions accordingly
        button_y = input_y_start + 3 * input_spacing + 50
        self.submit_button = ui.Button(screen, Config.width // 2, button_y + 30, 100, 60, "Register" if is_register else "Login")
        self.cancel_button = ui.Button(screen, Config.width // 2, button_y + 100 , 100, 60, "Cancel")

        # Labels
        self.font = pygame.font.Font('assets/font/KnightWarrior-w16n8.ttf', 26)
        self.username_label = self.font.render("Username:", True, (0, 0, 0))
        self.password_label = self.font.render("Password:", True, (0, 0, 0))
        self.email_label = self.font.render("Email:", True, (0, 0, 0)) if is_register else None

    def handle_events(self, event):
        self.username_input.handle_event(event)
        self.password_input.handle_event(event)
        if self.is_register and self.email_input:
            self.email_input.handle_event(event)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.submit_button.get_rect().collidepoint(event.pos):
                    sounds.button_sound.play()
                    if self.is_register:
                        if self.email_input:
                            return (self.username_input.text, self.password_input.text, self.email_input.text)
                        else:
                            print("Error: Email input is missing in register mode")
                            return None
                    else:
                        return (self.username_input.text, self.password_input.text)
                elif self.cancel_button.get_rect().collidepoint(event.pos):
                    sounds.button_sound.play()
                    return 'cancel'

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Draw labels above the input boxes
        self.screen.blit(self.username_label, (Config.width // 2 - 110, self.username_input.rect.y - 30))
        self.screen.blit(self.password_label, (Config.width // 2 - 110, self.password_input.rect.y - 30))
        if self.is_register and self.email_input:
            self.screen.blit(self.email_label, (Config.width // 2 - 110, self.email_input.rect.y - 30))

        self.username_input.draw()
        self.password_input.draw()
        if self.is_register and self.email_input:
            self.email_input.draw()
        self.submit_button.Draw()
        self.cancel_button.Draw()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                result = self.handle_events(event)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        return 'main'
                if result:
                    if result == 'cancel':
                        return 'main'
                    return result

            self.screen.blit(self.background, (0, 0))
            self.draw()

            pygame.display.flip()