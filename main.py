import pygame
import sys
from setting import Config
from MainScreen.menu  import Menu
from MainScreen.playmenu import PlayMenu
from MainScreen.optionmenu import OptionMenu
from MainScreen.loadmenu import LoadMenu
from MainScreen.botsmenu import BotsMenu
from MainScreen.leaderboardmenu import LeaderboardMenu
def main():
    pygame.init()
    screen = pygame.display.set_mode(Config.resolution)

    current_screen = 'main'
    while current_screen != 'exit':
        if current_screen == 'main':
            menu = Menu(screen)
        elif current_screen == 'play':
            menu = PlayMenu(screen)
        elif current_screen == 'bots':
            menu = BotsMenu(screen)
        elif current_screen == 'load':
            menu = LoadMenu(screen)
        elif current_screen == 'option':
            menu = OptionMenu(screen)
        elif current_screen == 'leaderboard':
            menu = LeaderboardMenu(screen)
        else:
            break

        current_screen = menu.Run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
