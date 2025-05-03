import pygame
import random
import json
from constants import *

class DialogueSystem:
    def __init__(self):
        self.personalities = self.load_personalities()
        self.active_monologue = None
        self.current_npc_id = None
        self.font = font_small
        self.dialogue_visible = False
    
    def load_personalities(self):
        with open("assets/personalities.json", "r", encoding="utf-8") as file:
            return json.load(file)
    
    def get_monologue(self, npc_id):
        for personality in self.personalities:
            if personality["id"] == npc_id:
                return random.choice(personality["monologues"])
        return "..."
    
    def toggle_dialogue(self, npc_id):
        if self.dialogue_visible and self.current_npc_id == npc_id:
            # Закрываем диалог, если открыт для этого же NPC
            self.close_dialogue()
        else:
            # Открываем новый диалог
            self.current_npc_id = npc_id
            self.active_monologue = self.get_monologue(npc_id)
            self.dialogue_visible = True
    
    def close_dialogue(self):
        """Закрывает текущий диалог"""
        self.dialogue_visible = False
        self.active_monologue = None
        self.current_npc_id = None
    
    def update(self, player, npcs):
        """Проверяет расстояние до NPC и закрывает диалог, если игрок слишком далеко"""
        if not self.dialogue_visible or self.current_npc_id is None:
            return
        
        # Находим NPC с текущим ID
        current_npc = None
        for npc in npcs:
            if npc.personality_id == self.current_npc_id:
                current_npc = npc
                break
        
        if current_npc:
            # Рассчитываем расстояние между игроком и NPC
            distance = ((player.rect.centerx - current_npc.rect.centerx)**2 + 
                       (player.rect.centery - current_npc.rect.centery)**2)**0.5
            
            if distance > DIALOGUE_RADIUS:
                self.close_dialogue()
    
    def draw(self, screen):
        if not self.dialogue_visible:
            return

        # Рассчитываем размеры панели
        text_width = min(SCREEN_WIDTH - 100, 600)
        text_height = 120
        pos_x = (SCREEN_WIDTH - text_width) // 2
        pos_y = SCREEN_HEIGHT - text_height - 20

        # Создаем полупрозрачную панель
        panel = pygame.Surface((text_width, text_height), pygame.SRCALPHA)
        panel.fill(DIALOGUE_BG_COLOR)
        
        # Рендерим текст с переносом строк
        wrapped_text = []
        words = self.active_monologue.split()
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.font.size(test_line)[0] < text_width - 40:
                current_line = test_line
            else:
                wrapped_text.append(current_line)
                current_line = word
        if current_line:
            wrapped_text.append(current_line)
        
        # Отрисовываем
        screen.blit(panel, (pos_x, pos_y))
        for i, line in enumerate(wrapped_text):
            text = self.font.render(line, True, DIALOGUE_TEXT_COLOR)
            screen.blit(text, (pos_x + 20, pos_y + 20 + i * 25))