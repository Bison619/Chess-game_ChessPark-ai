import pygame
import sys
from setting import Config
from menu import Menu

def main():
    pygame.init()
    screen = pygame.display.set_mode(Config.resolution)

    # Game loop
    menu_screen = Menu(screen)
    menu_screen.Run()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
