import pygame

def fade_out(screen, color=(0, 0, 0), duration=500):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface = fade_surface.convert()
    fade_surface.fill(color)

    for alpha in range(0, 150, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(duration // 150)

def fade_in(screen, color=(0, 0, 0), duration=500):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface = fade_surface.convert()
    fade_surface.fill(color)

    for alpha in range(255, 100, -5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(duration // 155)