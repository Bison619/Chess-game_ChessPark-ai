import pygame
from setting import sounds

class TextUI:
    def __init__(self, screen, text, x, y, fontSize, color):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.fontSize = fontSize
        self.color = color
        self.textColor = color
        self.font = pygame.font.Font("./assets/font/KnightWarrior-w16n8.ttf", self.fontSize)
        self.centered = False

    def Draw(self):
        mytext = self.font.render(self.text, True, self.textColor)

        if self.centered:
            text_rect = mytext.get_rect(center=(self.x , self.y))
            self.screen.blit(mytext, text_rect)
        else:
            self.screen.blit(mytext, (self.x, self.y))

class Text2UI:
    def __init__(self, screen, text, x, y, fontSize, color):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.fontSize = fontSize
        self.color = color
        self.textColor = color
        self.font = pygame.font.Font("./assets/font/Roboto-Bold.ttf", self.fontSize)
        self.centered = False

    def Draw(self):
        lines = self.text.split("\n")
        for i, line in enumerate(lines):
            mytext = self.font.render(line, True, self.textColor)
            if self.centered:
                text_rect = mytext.get_rect(center=(self.x, self.y + i * self.fontSize))
                self.screen.blit(mytext, text_rect)
            else:
                self.screen.blit(mytext, (self.x, self.y + i * self.fontSize))

class Button:
    def __init__(self, screen, x, y, w, h, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w + 100
        self.h = h
        self.text = text
        self.thickness = 4
        self.backgroundColor = (72, 61, 139)
        self.outlineColor = (123, 104, 238)
        self.textColor = (255, 255, 255)
        self.hoverColor = (106, 90, 205)
        self.shadowColor = (44, 44, 84)
        self.fontSize = 50
        self.font = pygame.font.Font("./assets/font/KnightWarrior-w16n8.ttf", self.fontSize)
        self.tempcolor = self.backgroundColor
        self.counter = 0

    def Hover(self):
        mouse_position = pygame.mouse.get_pos()
        if self.get_rect().collidepoint(mouse_position):
            self.tempcolor = self.hoverColor
            self.counter += 1
            if self.counter == 2:
                sounds.castle_sound.play()
        else:
            self.counter = 0
            self.tempcolor = self.backgroundColor

    def get_rect(self):
        x = self.x - self.w // 2 - self.thickness // 2
        y = self.y - self.h // 2 - self.thickness // 2
        w = self.w + self.thickness
        h = self.h + self.thickness
        return pygame.Rect(x, y, w, h)

    def Draw(self):
        # added shadow for the button
        shadow_offset = 5
        pygame.draw.rect(self.screen, self.shadowColor, [self.x - self.w // 2 + shadow_offset, self.y - self.h // 2 + shadow_offset, self.w, self.h], border_radius=20)

        # for the outer border of the button for stroke
        out_x = self.x - self.w // 2 - self.thickness // 2
        out_y = self.y - self.h // 2 - self.thickness // 2
        out_w = self.w + self.thickness
        out_h = self.h + self.thickness
        pygame.draw.rect(self.screen, self.outlineColor, [out_x, out_y, out_w, out_h], border_radius=20)

        # Inner fill of the button
        in_x = self.x - self.w // 2
        in_y = self.y - self.h // 2
        in_w = self.w
        in_h = self.h
        pygame.draw.rect(self.screen, self.tempcolor, [in_x, in_y, in_w, in_h], border_radius=20)

        # Button text
        buttonText = self.font.render(self.text, True, self.textColor)
        text_rect = buttonText.get_rect(center=(self.x, self.y))
        self.screen.blit(buttonText, text_rect)

        self.Hover()


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)