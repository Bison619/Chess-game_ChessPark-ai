import pygame
from setting import Config, sounds
from MainScreen.fadeeffect import fade_out
import ui

class RuleMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg2blur.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)
        self.running = True
        self.clock = pygame.time.Clock()

        # Load and scale the rules image
        original_image = pygame.image.load("assets/images/chess_cheat_sheet_.jpg")
        image_aspect_ratio = original_image.get_width() / original_image.get_height()
        new_height = Config.resolution[1] * 12
        new_width = int(new_height * image_aspect_ratio)
        self.rules_image = pygame.transform.smoothscale(original_image, (new_width, new_height))

        self.image_rect = self.rules_image.get_rect()
        self.scroll_y = 0
        self.scroll_speed = 60

        # Calculate x position to center the image
        self.image_x = (Config.resolution[0] - new_width) // 2

        # Button
        button_y_start = Config.height // 2 - 20
        button_spacing = 110
        self.back = ui.Button(screen, Config.width // 2 + 680, button_y_start + 3.7 * button_spacing, 40, 60, "Back")

    def GetFrameRate(self):
        return self.clock.get_fps()

    def display_rules(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.rules_image, (self.image_x, self.scroll_y))
        self.DrawButtons()

    def DrawButtons(self):
        self.back.Draw()

    def HandleClick(self, screen):
        mouse_position = pygame.mouse.get_pos()
        if self.back.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            return 'option'
        return None

    def Run(self):
        while self.running:
            self.clock.tick(Config.fps)
            pygame.display.set_caption("Chess " + str(int(self.GetFrameRate())))

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
                elif event.type == pygame.MOUSEWHEEL:
                    self.scroll_y += event.y * self.scroll_speed
                    # Limit scrolling
                    max_scroll = min(0, Config.resolution[1] - self.image_rect.height)
                    self.scroll_y = max(max_scroll, min(0, self.scroll_y))

            self.display_rules()
            pygame.display.update()