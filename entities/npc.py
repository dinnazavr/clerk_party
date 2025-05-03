import pygame
from constants import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, color_idx, personality_id):
        super().__init__()
        # Убедимся, что NPC не появляется в зоне инвентаря
        if y < INVENTORY_HEIGHT + 10:  # +10 для запаса
            y = INVENTORY_HEIGHT + 10
        self.image = pygame.Surface((30, 50))
        self.image.fill(COLORS[color_idx % len(COLORS)])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.personality_id = personality_id