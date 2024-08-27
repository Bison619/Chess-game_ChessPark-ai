import pygame
import ui
import requests
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
        self.fetch_leaderboard_data()
        self.leaderboard_data = []

        # Button
        button_y_start = Config.height // 2 - 20
        button_spacing = 110
        self.back = ui.Button(screen, Config.width // 2, button_y_start + 3.6 * button_spacing, 120, 60, "Back")
        self.refresh = ui.Button(screen, Config.width // 2 + 640, button_y_start + 3.6 * button_spacing, 120, 60, "Refresh")

        self.running = True
        self.clock = pygame.time.Clock()
        self.chess = Chess(screen)

        #  (dummy data for now unitl backend)
        # self.leaderboard_data = [
        #     ("1", "Alice", "1500"),
        #     ("2", "Bob", "1400"),
        #     ("3", "Charlie", "1300"),
        #     ("4", "David", "1200"),
        #     ("5", "Eva", "1100"),
        #     ("6", "Frank", "1000"),
        #     ("7", "Grace", "900"),
        #     ("8", "Hank", "800"),
        # ]

    def fetch_leaderboard_data(self):
        try:
            response = requests.get('http://localhost:8000/authentication/get_leaderboard/')
            if response.status_code == 200:
                data = response.json()

                if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                    # Sort the data by points in descending order
                    sorted_data = sorted(data, key=lambda x: x.get('points', 0), reverse=True)

                    self.leaderboard_data = [
                        (str(i+1), entry.get('username', ''), str(entry.get('points', 0)))
                        for i, entry in enumerate(sorted_data[:8])  # Limit to top 8
                    ]
                else:
                    print("Unexpected data format:", data)
                    self.leaderboard_data = []
            else:
                print("Failed to fetch leaderboard data. Status code:", response.status_code)
                self.leaderboard_data = []
        except Exception as e:
            print(f"Error fetching leaderboard data: {e}")
            self.leaderboard_data = []

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

        # Use the fetched leaderboard data
        for index, entry in enumerate(self.leaderboard_data):
            if index >= 8:
                break
            y_position = leaderboard_rect.y + entry_y_start + index * entry_y_spacing
            color = (255, 215, 0) if index == 0 else (192, 192, 192) if index == 1 else (205, 127, 50) if index == 2 else (255, 255, 255)

            for i, text in enumerate(entry):
                entry_text = TextUI(self.screen, text, middle_x + header_offsets[i], y_position, 28, color)
                entry_text.centered = True
                entry_text.Draw()

        # If there are fewer than 8 entries, fill the rest with empty rows
        for index in range(len(self.leaderboard_data), 8):
            y_position = leaderboard_rect.y + entry_y_start + index * entry_y_spacing
            for i in range(3):
                entry_text = TextUI(self.screen, "-", middle_x + header_offsets[i], y_position, 28, (255, 255, 255))
                entry_text.centered = True
                entry_text.Draw()

        separator_y = leaderboard_rect.bottom - 70
        pygame.draw.line(self.screen, (255, 255, 255), (leaderboard_rect.left + 20, separator_y), (leaderboard_rect.right - 20, separator_y), 2)
        self.draw_logged_in_user()

    def DrawButtons(self):
        self.header_text.Draw()
        self.back.Draw()
        self.refresh.Draw()

    def draw_logged_in_user(self):
        if Menu.is_logged_in and Menu.logged_in_user:
            leaderboard_rect = pygame.Rect(250, 140, Config.width - 500, Config.height - 300)
            user_y_position = leaderboard_rect.bottom - 50
            middle_x = leaderboard_rect.x + leaderboard_rect.width // 2
            header_offsets = [-200, 0, 200]

            user_points = '-'

            user_data = ["-", Menu.logged_in_user, str(user_points)]
            for i, text in enumerate(user_data):
                entry_text = TextUI(self.screen, text, middle_x + header_offsets[i], user_y_position, 28, (0, 255, 0))
                entry_text.centered = True
                entry_text.Draw()

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
        elif self.refresh.get_rect().collidepoint(mouse_position):
            sounds.button_sound.play()
            self.fetch_leaderboard_data()

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
            self.draw_logged_in_user()
            pygame.display.update()
