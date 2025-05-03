import pygame
from constants import *
from ui.personality_selector import PersonalitySelector

def character_selection(screen):
    selector = PersonalitySelector()
    selected_personality = None

    while selected_personality is None:
        screen.fill(WHITE)
        result = selector.draw(screen)
        if result == "menu":
            return "menu"
        elif isinstance(result, dict):
            selected_personality = result
        pygame.display.flip()

    return selected_personality