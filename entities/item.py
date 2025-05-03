import pygame
import random
from constants import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.image = pygame.Surface((ITEM_SIZE, ITEM_SIZE))
        self.type = item_type
        
        # Разные цвета для разных типов предметов
        colors = {
            "weapon": (255, 0, 0),
            "potion": (0, 255, 0),
            "scroll": (0, 0, 255),
            "food": (255, 255, 0)
        }
        self.image.fill(colors.get(item_type, (255, 255, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y