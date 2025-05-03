import sys
import pygame
import json
from constants import *
from ui.buttons import Button


class PersonalitySelector:
    def __init__(self):
        self.personalities = []
        self.current_index = 0
        self.load_personalities()

    def load_personalities(self):
        with open("assets/personalities.json", "r", encoding="utf-8") as file:
            self.personalities = json.load(file)

    def next_personality(self):
        self.current_index = (self.current_index + 1) % len(self.personalities)

    def prev_personality(self):
        self.current_index = (self.current_index - 1) % len(self.personalities)

    def get_current_personality(self):
        return self.personalities[self.current_index]

    def draw_mbti_table(self, surface, mbti_type, x, y):
        dimensions = [
            ("I (Интроверт)", "E (Экстраверт)"),
            ("N (Интуитивные)", "S (Реалистичные)"),
            ("T (Логика)", "F (Принципы)"),
            ("J (Планирующие)", "P (Ищущие)"),
        ]

        active_traits = [
            0 if mbti_type[0] == "I" else 1,
            0 if mbti_type[1] == "N" else 1,
            0 if mbti_type[2] == "T" else 1,
            0 if mbti_type[3] == "J" else 1,
        ]

        cell_width = 170
        cell_height = 30
        header_height = 35
        table_width = cell_width * 2
        table_height = header_height + cell_height * len(dimensions)

        # Фон таблицы
        pygame.draw.rect(
            surface, LIGHT_GRAY, (x, y, table_width, table_height), border_radius=10
        )
        pygame.draw.rect(
            surface, BLACK, (x, y, table_width, table_height), 2, border_radius=10
        )

        # Заголовок таблицы
        header = font_medium.render("Характеристики личности", True, BLACK)
        surface.blit(header, (x + (table_width - header.get_width()) // 2, y + 10))

        # Отрисовка таблицы
        for i, (left, right) in enumerate(dimensions):
            y_pos = y + header_height + i * cell_height

            # Левая ячейка
            left_color = DARK_BLUE if active_traits[i] == 0 else LIGHT_GRAY
            pygame.draw.rect(
                surface,
                left_color,
                (x, y_pos, cell_width, cell_height),
                border_radius=5,
            )
            pygame.draw.rect(
                surface, BLACK, (x, y_pos, cell_width, cell_height), 2, border_radius=5
            )
            left_text = font_small.render(
                left, True, BLACK if active_traits[i] != 0 else WHITE
            )
            surface.blit(
                left_text, (x + 20, y_pos + (cell_height - left_text.get_height()) // 2)
            )

            # Правая ячейка
            right_color = DARK_BLUE if active_traits[i] == 1 else LIGHT_GRAY
            pygame.draw.rect(
                surface,
                right_color,
                (x + cell_width, y_pos, cell_width, cell_height),
                border_radius=5,
            )
            pygame.draw.rect(
                surface,
                BLACK,
                (x + cell_width, y_pos, cell_width, cell_height),
                2,
                border_radius=5,
            )
            right_text = font_small.render(
                right, True, BLACK if active_traits[i] != 1 else WHITE
            )
            surface.blit(
                right_text,
                (
                    x + cell_width + 20,
                    y_pos + (cell_height - right_text.get_height()) // 2,
                ),
            )

    def draw(self, surface):
        personality = self.get_current_personality()

        # Основная панель
        main_panel = pygame.Rect(260, 110, 1400, 785)
        pygame.draw.rect(surface, LIGHT_GRAY, main_panel, border_radius=20)
        pygame.draw.rect(surface, BLACK, main_panel, 3, border_radius=20)

        # Кнопки листания
        prev_button = Button(500, SCREEN_HEIGHT // 2 - 160, 80, 50, "<", GRAY, BLUE)
        next_button = Button(
            SCREEN_WIDTH - 580, SCREEN_HEIGHT // 2 - 160, 80, 50, ">", GRAY, BLUE
        )
        select_button = Button(
            SCREEN_WIDTH // 2 - 150, 900, 300, 60, "Выбрать", GRAY, BLUE
        )  # Подняли кнопку выше

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        esc_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.prev_personality()
                if event.key == pygame.K_RIGHT:
                    self.next_personality()
                if event.key == pygame.K_ESCAPE:
                    esc_pressed = True

        if esc_pressed:
            return "menu"  # Возвращаемся в меню при нажатии ESC

        prev_button.check_hover(mouse_pos)
        next_button.check_hover(mouse_pos)
        select_button.check_hover(mouse_pos)

        if prev_button.is_clicked(mouse_pos, mouse_click):
            self.prev_personality()
        if next_button.is_clicked(mouse_pos, mouse_click):
            self.next_personality()
        if select_button.is_clicked(mouse_pos, mouse_click):
            return personality

        # Отрисовка кнопок
        prev_button.draw(surface)
        next_button.draw(surface)
        select_button.draw(surface)

        # Изображение персонажа
        image_x = SCREEN_WIDTH // 2 - 200
        image_y = 170  # Подняли изображение выше
        try:
            image = pygame.image.load(personality["image"])
            image = pygame.transform.scale(image, (400, 400))
            surface.blit(image, (image_x, image_y))
        except:
            placeholder = pygame.Surface((400, 400))
            placeholder.fill((100, 100, 200))
            surface.blit(placeholder, (image_x, image_y))

        # Название типа
        type_text = font_large.render(personality["name"], True, BLACK)
        surface.blit(type_text, (SCREEN_WIDTH // 2 - type_text.get_width() // 2, 560))

        # Таблица характеристик MBTI
        table_x = SCREEN_WIDTH // 2 - 175
        table_y = 610
        self.draw_mbti_table(surface, personality["mbti"], table_x, table_y)

        # Описание персонажа
        desc_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 400, 790, 800, 80
        )  # Уменьшили высоту описания
        pygame.draw.rect(surface, LIGHT_GRAY, desc_rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, desc_rect, 2, border_radius=10)

        desc_lines = []
        words = personality["description"].split()
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font_small.size(test_line)[0] < desc_rect.width - 40:
                current_line = test_line
            else:
                desc_lines.append(current_line)
                current_line = word + " "
        desc_lines.append(current_line)

        for i, line in enumerate(desc_lines[:2]):  # Ограничили до 2 строк
            line_surface = font_small.render(line, True, BLACK)
            surface.blit(line_surface, (desc_rect.x + 20, desc_rect.y + 15 + i * 30))

        return None