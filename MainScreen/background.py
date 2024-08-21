import pygame

class Background:
    def __init__(self, screen):
        self.screen = screen
        self.bg_image = pygame.image.load("assets/images/sakura.png").convert_alpha()
        self.bg_width, self.bg_height =  [int(x * 0.70) for x in self.screen.get_size()]
        self.bg_image = pygame.transform.scale(self.bg_image, (self.bg_width, self.bg_height))
        self.bg_x1 = -60
        self.bg_x2 = self.bg_width
        self.scroll_speed = 1

    def draw(self):
        self.bg_x1 -= self.scroll_speed
        self.bg_x2 -= self.scroll_speed

        if self.bg_x1 < -self.bg_width:
            self.bg_x1 = self.bg_width
        if self.bg_x2 < -self.bg_width:
            self.bg_x2 = self.bg_width

        self.screen.blit(self.bg_image, (self.bg_x1, 0))
        self.screen.blit(self.bg_image, (self.bg_x2, 0))