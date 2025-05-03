import pygame
import sys
from constants import *
from states.menu import main_menu
from states.character_select import character_selection
from states.game import game_loop

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Clerk Party")

    current_screen = "menu"
    selected_personality = None

    while True:
        if current_screen == "menu":
            menu_result = main_menu(screen)
            if menu_result == "select_character":
                current_screen = "select_character"
            else:
                break
        elif current_screen == "select_character":
            result = character_selection(screen)
            if result == "menu":
                current_screen = "menu"
            else:
                selected_personality = result
                current_screen = "game"
        elif current_screen == "game":
            game_result = game_loop(screen, selected_personality)
            if game_result == "menu":
                current_screen = "menu"

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
