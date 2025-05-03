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
    clock = pygame.time.Clock()

    while True:
        if current_screen == "menu":
            menu_result = main_menu(screen)
            if menu_result == "select_character":
                current_screen = "select_character"
            elif menu_result == "quit":
                break

        elif current_screen == "select_character":
            screen.fill(WHITE)
            pygame.display.flip()
            
            result = character_selection(screen)
            if result == "menu":
                current_screen = "menu"
            elif isinstance(result, dict):
                selected_personality = result
                current_screen = "game"
                # Небольшая задержка для плавного перехода
                pygame.time.delay(100)

        elif current_screen == "game":
            game_result = game_loop(screen, selected_personality)
            if game_result == "menu":
                current_screen = "menu"
            elif game_result == "quit":
                running = False  # Полный выход из игры

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
