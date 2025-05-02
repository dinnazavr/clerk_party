import pygame
import sys
import json
import os
import random

pygame.init()

# Настройки окна
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Clerk Party")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE = (100, 150, 255)
DARK_BLUE = (70, 100, 200)
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (128, 0, 0),
    (0, 128, 0),
    (0, 0, 128),
    (128, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (192, 192, 192),
    (128, 128, 128),
    (255, 165, 0),
]

# Шрифты
font_small = pygame.font.SysFont("Arial", 20)
font_medium = pygame.font.SysFont("Arial", 24)
font_large = pygame.font.SysFont("Arial", 32)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)

        text_surface = font_medium.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((8, 8, 8))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.prev_x = x
        self.prev_y = y

    def update(self, keys):
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        # Жесткое ограничение границ
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))


class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, color_idx):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(COLORS[color_idx % len(COLORS)])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def generate_npcs(count, player):
    npcs = []
    occupied_areas = [player.rect.copy()]  # Начинаем с области игрока

    for i in range(count):
        attempts = 0
        placed = False

        while attempts < 1000 and not placed:
            x = random.randint(0, SCREEN_WIDTH - 30)
            y = random.randint(0, SCREEN_HEIGHT - 50)
            new_rect = pygame.Rect(x, y, 30, 50)

            # Проверяем отступы от других объектов (минимум 5 пикселей)
            collision = False
            for area in occupied_areas:
                if new_rect.colliderect(area.inflate(10, 10)):  # Добавляем отступы
                    collision = True
                    break

            if not collision:
                npc = NPC(x, y, i)
                npcs.append(npc)
                occupied_areas.append(new_rect)
                placed = True

            attempts += 1

        if not placed:
            # Если не удалось найти место, размещаем в углу с проверкой
            corners = [
                (10, 10),
                (SCREEN_WIDTH - 40, 10),
                (10, SCREEN_HEIGHT - 60),
                (SCREEN_WIDTH - 40, SCREEN_HEIGHT - 60),
            ]
            for corner in corners:
                corner_rect = pygame.Rect(corner[0], corner[1], 30, 50)
                collision = False
                for area in occupied_areas:
                    if corner_rect.colliderect(area.inflate(10, 10)):
                        collision = True
                        break
                if not collision:
                    npc = NPC(corner[0], corner[1], i)
                    npcs.append(npc)
                    occupied_areas.append(corner_rect)
                    placed = True
                    break

    return npcs


class PersonalitySelector:
    def __init__(self):
        self.personalities = []
        self.current_index = 0
        self.load_personalities()

    def load_personalities(self):
        with open("personalities.json", "r", encoding="utf-8") as file:
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


def main_menu():
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


def character_selection():
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


def game_loop(selected_personality):
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    npcs = generate_npcs(15, player)

    all_sprites = pygame.sprite.Group(player, *npcs)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        player.update(keys)

        # Проверка столкновений с NPC
        for npc in npcs:
            if player.rect.colliderect(npc.rect):
                player.rect.x = player.prev_x
                player.rect.y = player.prev_y

        screen.fill(WHITE)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return "menu"


def main():
    current_screen = "menu"
    selected_personality = None

    while True:
        if current_screen == "menu":
            menu_result = main_menu()
            if menu_result == "select_character":
                current_screen = "select_character"
            else:
                break
        elif current_screen == "select_character":
            result = character_selection()
            if result == "menu":
                current_screen = "menu"
            else:
                selected_personality = result
                current_screen = "game"
        elif current_screen == "game":
            game_result = game_loop(selected_personality)
            if game_result == "menu":
                current_screen = "menu"

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
