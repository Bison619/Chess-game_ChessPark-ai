import pygame
import requests
import json

class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()
        self.input_box = pygame.Rect(100, 100, 140, 32)
        self.active = False
        self.text = ''
        self.done = False

    def get_input(self, prompt):
        input_box = pygame.Rect(100, 100, 140, 32)
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill((30, 30, 30))
            txt_surface = self.font.render(prompt + text, True, (255, 255, 255))
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)

            pygame.display.flip()
            self.clock.tick(30)

    def register(self):
        username = self.get_input('Enter username: ')
        password = self.get_input('Enter password: ')
        email = self.get_input('Enter email: ')

        data = {
            'username': username,
            'password': password,
            'email': email
        }
        response = requests.post('http://127.0.0.1:8000/auth/register/', data=json.dumps(data))
        if response.json().get('status') == 'success':
            print('Registration successful')
        else:
            print('Registration failed:', response.json().get('message'))

    def login(self):
        username = self.get_input('Enter username: ')
        password = self.get_input('Enter password: ')

        data = {
            'username': username,
            'password': password
        }
        response = requests.post('http://127.0.0.1:8000/auth/login/', data=json.dumps(data))
        if response.json().get('status') == 'success':
            print('Login successful')
        else:
            print('Login failed:', response.json().get('message'))
