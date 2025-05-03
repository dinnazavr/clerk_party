import pygame
from constants import *
from ui.buttons import Button
import sys

def main_menu(screen):
    start_button = Button(
        SCREEN_WIDTH // 2 - 200, 500, 400, 100, "Начать игру", GRAY, BLUE
    )
    exit_button = Button(SCREEN_WIDTH // 2 - 200, 650, 400, 100, "Выход", GRAY, BLUE)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True

        start_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)

        if start_button.is_clicked(mouse_pos, mouse_click):
            return "select_character"
        if exit_button.is_clicked(mouse_pos, mouse_click):
            pygame.quit()
            sys.exit()

        screen.fill(WHITE)
        title_text = font_large.render("Clerk Party", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 300))
        start_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()