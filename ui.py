import pygame

class Button:
    def __init__(self, screen, x, y, w, h, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w + 100
        self.h = h
        self.text = text
        self.thickness = 4
        self.backgroundColor = (51, 255, 59)
        self.outlineColor = (27, 133, 31)
        self.textColor = (255 ,255, 255)
        self.hoverColor = (27, 133, 31)
        self.fontSize = 50
        self.font = pygame.font.Font("./assets/font/KnightWarrior-w16n8.ttf", self.fontSize)
        self.tempcolor = self.backgroundColor
        self.counter = 0

    def Hover(self):

        mouse_position = pygame.mouse.get_pos()
        # return 0 or 1
        if self.get_rect().collidepoint(mouse_position):
            self.tempcolor = self.hoverColor
            self.counter += 1
            if self.counter == 2:
                pass
                # sounds.check_sound.play()
        else:
            self.counter = 0
            self.tempcolor = self.backgroundColor

    def get_rect(self):
        x = self.x - self.w//2 - self.thickness//2
        y = self.y - self.h //2 - self.thickness//2
        w = self.w + self.thickness
        h = self.h + self.thickness
        return pygame.Rect(x, y, w, h)

    def Draw(self):
        out_x = self.x - self.w//2 - self.thickness//2
        out_y = self.y - self.h //2 - self.thickness//2
        out_w = self.w + self.thickness
        out_h = self.h + self.thickness

        in_x = self.x - self.w //2
        in_y = self.y - self.h //2
        in_w = self.w
        in_h = self.h
        pygame.draw.rect(self.screen, self.outlineColor, [out_x, out_y, out_w, out_h], border_radius=20)
        pygame.draw.rect(self.screen, self.tempcolor, [in_x, in_y, in_w, in_h], border_radius=20)
        buttonText = self.font.render(self.text, True, self.textColor)
        text_rect = buttonText.get_rect(center=(in_x + self.w//2, in_y + self.h//2))
        self.screen.blit(buttonText, text_rect)

        self.Hover()