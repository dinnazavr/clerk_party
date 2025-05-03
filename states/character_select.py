import pygame
from constants import *
from ui.personality_selector import PersonalitySelector

def character_selection(screen):
    selector = PersonalitySelector()
    selected_personality = None
    clock = pygame.time.Clock()  # Добавляем часы для контроля FPS

    while selected_personality is None:
        # Очищаем экран перед каждой отрисовкой
        screen.fill(WHITE)
        
        result = selector.draw(screen)
        
        if result == "menu":
            return "menu"
        elif isinstance(result, dict):
            selected_personality = result
            
        pygame.display.flip()
        clock.tick(60)  # Ограничиваем FPS

    # После выбора персонажа очищаем экран
    screen.fill(WHITE)
    pygame.display.flip()
    
    return selected_personality