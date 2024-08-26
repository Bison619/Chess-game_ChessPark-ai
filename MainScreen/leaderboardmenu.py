import pygame
import ui
from setting import Config, sounds
from MainScreen.chess import Chess
from MainScreen.fadeeffect import fade_out
from ui import TextUI
from MainScreen.menu import Menu

class LeaderboardMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("./assets/images/mainbg2blur.png")
        self.background = pygame.transform.smoothscale(self.background, Config.resolution)
        self.header_text = TextUI(screen, "Leaderboard", Config.width // 2 - 150, 30, 64, (255, 255, 255))

        # Button
        button_y_start = Config.height // 2 - 20
        button_spacing = 110
        self.back = ui.Button(screen, Config.width // 2, button_y_start + 3.6 * button_spacing, 200, 60, "Back")

        self.running = True
        self.clock = pygame.time.Clock()
        self.chess = Chess(screen)

        #  (dummy data for now unitl backend)
        self.leaderboard_data = [
            ("1", "Alice", "1500"),
            ("2", "Bob", "1400"),
            ("3", "Charlie", "1300"),
            ("4", "David", "1200"),
            ("5", "Eva", "1100"),
            ("6", "Frank", "1000"),
            ("7", "Grace", "900"),
            ("8", "Hank", "800"),
        ]

    def DrawLeaderboard(self):
        border_radius = 20
        leaderboard_rect = pygame.Rect(250, 140, Config.width - 500, Config.height - 300)
        pygame.draw.rect(self.screen, (44, 62, 80), leaderboard_rect, border_radius=border_radius)
        header_y_offset = 20
        entry_y_start = 60
        entry_y_spacing = 40
        middle_x = leaderboard_rect.x + leaderboard_rect.width // 2
        header_offsets = [-200, 0, 200]

        # Center headers and entries
        for i, header in enumerate(["S.N", "Name", "Score"]):
            header_text = TextUI(self.screen, header, middle_x + header_offsets[i], leaderboard_rect.y + header_y_offset, 36, (255, 255, 255))
            header_text.centered = True
            header_text.Draw()

        for index, entry in enumerate(self.leaderboard_data):
            y_position = leaderboard_rect.y + entry_y_start + index * entry_y_spacing
            color = (255, 215, 0) if index == 0 else (192, 192, 192) if index == 1 else (205, 127, 50) if index == 2 else (255, 255, 255)

            for i, text in enumerate(entry):
                entry_text = TextUI(self.screen, text, middle_x + header_offsets[i], y_position, 28, color)
                entry_text.centered = True
                entry_text.Draw()

    def DrawButtons(self):
        self.header_text.Draw()
        self.back.Draw()

    def draw_username(self):
        if Menu.is_logged_in and Menu.logged_in_user:
            font = pygame.font.Font('assets/font/KnightWarrior-w16n8.ttf', 32)
            text_surface = font.render(f"Player : {Menu.logged_in_user}", True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.topright = (Config.width - 40, 30)
            self.screen.blit(text_surface, text_rect)

    def HandleClick(self, screen):
        mouse_position = pygame.mouse.get_pos()

        if self.back.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            fade_out(screen)
            return 'option'

    def GetFrameRate(self):
        return self.clock.get_fps()

    def Run(self):
        while self.running:
            self.clock.tick(Config.fps)
            pygame.display.set_caption("Chess " + str(int(self.GetFrameRate())))
            self.screen.blit(self.background, (0, 0))
            # handle Events
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
            self.DrawButtons()
            self.DrawLeaderboard()
            self.draw_username()
            pygame.display.update()
