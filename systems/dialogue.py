import pygame
import random
import json
from constants import *

class DialogueSystem:
    def __init__(self):
        self.personalities = self.load_personalities()
        self.active_monologue = None
        self.current_npc = None
        self.font = font_small
        self.dialogue_visible = False
        self.guessing_mode = False
        self.player_guess = [None, None, None, None]
        self.guess_table_pos = (SCREEN_WIDTH//2 - 175, SCREEN_HEIGHT//2 - 100)
        self.last_interaction_time = 0
        self.guess_feedback = ""
        self.feedback_timer = 0

    def load_personalities(self):
        with open("assets/personalities.json", "r", encoding="utf-8") as file:
            return json.load(file)

    def get_monologue(self, npc_id):
        for personality in self.personalities:
            if personality["id"] == npc_id:
                return random.choice(personality["monologues"])
        return "..."

    def start_dialogue(self, npc):
        if self.guessing_mode:
            return
            
        self.current_npc = npc
        self.active_monologue = self.get_monologue(npc.personality_id)
        self.dialogue_visible = True
        self.last_interaction_time = pygame.time.get_ticks()
        self.guessing_mode = False
        self.player_guess = [None, None, None, None]

    def start_guessing(self):
        if not self.dialogue_visible or not self.current_npc:
            return
            
        self.guessing_mode = True
        self.player_guess = [None, None, None, None]
        self.last_interaction_time = pygame.time.get_ticks()

    def close_dialogue(self):
        self.dialogue_visible = False
        self.guessing_mode = False
        self.active_monologue = None
        self.current_npc = None
        self.guess_feedback = ""
        self.feedback_timer = 0

    def handle_guess_click(self, pos):
        if not self.guessing_mode:
            return
            
        x, y = self.guess_table_pos
        cell_width = 170
        cell_height = 30
        header_height = 35
        
        if (x <= pos[0] <= x + cell_width*2 and 
            y + header_height <= pos[1] <= y + header_height + cell_height*4):
            
            row = (pos[1] - y - header_height) // cell_height
            col = (pos[0] - x) // cell_width
            
            if 0 <= row <= 3 and 0 <= col <= 1:
                self.player_guess[row] = col
                self.last_interaction_time = pygame.time.get_ticks()

    def check_guess(self):
        if not self.guessing_mode or None in self.player_guess or self.current_npc is None:
            return False
            
        npc_personality = next((p for p in self.personalities 
                            if p["id"] == self.current_npc.personality_id), None)
        
        if not npc_personality:
            return False
            
        mbti = npc_personality["mbti"]
        correct_answers = [
            0 if mbti[0] == "I" else 1,
            0 if mbti[1] == "N" else 1,
            0 if mbti[2] == "T" else 1,
            0 if mbti[3] == "J" else 1,
        ]
        
        is_correct = self.player_guess == correct_answers
        self.guess_feedback = "Правильно!" if is_correct else "Неверно!"
        self.feedback_timer = pygame.time.get_ticks()
        
        if is_correct:
            pygame.time.delay(1000)
            self.close_dialogue()
            
        return is_correct

    def update(self, player):
        current_time = pygame.time.get_ticks()
        
        # Автоматическое закрытие при бездействии
        if (self.dialogue_visible and 
            current_time - self.last_interaction_time > 15000):  # 15 секунд
            self.close_dialogue()
            return
            
        # Закрытие при отдалении от NPC
        if self.dialogue_visible and self.current_npc:
            distance = ((player.rect.centerx - self.current_npc.rect.centerx)**2 + 
                       (player.rect.centery - self.current_npc.rect.centery)**2)**0.5
            if distance > DIALOGUE_RADIUS * 1.5:  # Немного больший радиус
                self.close_dialogue()

    def draw_mbti_table(self, surface, guess_mode=False):
        dimensions = [
            ("I (Интроверт)", "E (Экстраверт)"),
            ("N (Интуитивные)", "S (Реалистичные)"),
            ("T (Логика)", "F (Принципы)"),
            ("J (Планирующие)", "P (Ищущие)"),
        ]
        
        x, y = self.guess_table_pos
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
        title = "Выберите характеристики" if guess_mode else "Характеристики личности"
        header = font_medium.render(title, True, BLACK)
        surface.blit(header, (x + (table_width - header.get_width()) // 2, y + 10))

        for i, (left, right) in enumerate(dimensions):
            y_pos = y + header_height + i * cell_height

            # Левая ячейка
            left_color = DARK_BLUE if self.player_guess[i] == 0 else LIGHT_GRAY
            pygame.draw.rect(
                surface, left_color, (x, y_pos, cell_width, cell_height), border_radius=5
            )
            pygame.draw.rect(
                surface, BLACK, (x, y_pos, cell_width, cell_height), 2, border_radius=5
            )
            left_text = font_small.render(
                left, True, BLACK if self.player_guess[i] != 0 else WHITE
            )
            surface.blit(
                left_text, (x + 20, y_pos + (cell_height - left_text.get_height()) // 2)
            )

            # Правая ячейка
            right_color = DARK_BLUE if self.player_guess[i] == 1 else LIGHT_GRAY
            pygame.draw.rect(
                surface, right_color, (x + cell_width, y_pos, cell_width, cell_height), 
                border_radius=5
            )
            pygame.draw.rect(
                surface, BLACK, (x + cell_width, y_pos, cell_width, cell_height), 
                2, border_radius=5
            )
            right_text = font_small.render(
                right, True, BLACK if self.player_guess[i] != 1 else WHITE
            )
            surface.blit(
                right_text,
                (x + cell_width + 20, y_pos + (cell_height - right_text.get_height()) // 2)
            )

        # Инструкция
        if guess_mode:
            instruction = font_small.render("Нажмите пробел для проверки", True, BLACK)
            surface.blit(instruction, (x, y + table_height + 10))
            
            # Обратная связь
            if self.guess_feedback and pygame.time.get_ticks() - self.feedback_timer < 2000:
                feedback_color = GREEN if "Правильно" in self.guess_feedback else RED
                feedback_text = font_small.render(self.guess_feedback, True, feedback_color)
                surface.blit(feedback_text, 
                            (x + table_width//2 - feedback_text.get_width()//2, 
                            y + table_height + 40))

    def draw(self, surface):
        if not self.dialogue_visible:
            return

        # Рисуем монолог
        text_width = min(SCREEN_WIDTH - 100, 600)
        text_height = 120
        pos_x = (SCREEN_WIDTH - text_width) // 2
        pos_y = SCREEN_HEIGHT - text_height - 20

        panel = pygame.Surface((text_width, text_height), pygame.SRCALPHA)
        panel.fill(DIALOGUE_BG_COLOR)
        
        words = self.active_monologue.split()
        wrapped_lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.font.size(test_line)[0] < text_width - 40:
                current_line = test_line
            else:
                wrapped_lines.append(current_line)
                current_line = word
        if current_line:
            wrapped_lines.append(current_line)
        
        surface.blit(panel, (pos_x, pos_y))
        for i, line in enumerate(wrapped_lines[:3]):  # Макс 3 строки
            text = self.font.render(line, True, DIALOGUE_TEXT_COLOR)
            surface.blit(text, (pos_x + 20, pos_y + 20 + i * 25))

        # Рисуем таблицу для угадывания
        if self.guessing_mode:
            self.draw_mbti_table(surface, guess_mode=True)
        else:
            # Кнопка для перехода к угадыванию
            prompt_text = font_small.render("Нажмите ПРОБЕЛ чтобы угадать тип", True, BLACK)
            surface.blit(prompt_text, (pos_x, pos_y - 30))