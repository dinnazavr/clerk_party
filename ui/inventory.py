import pygame
from constants import *

class InventoryUI:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, SCREEN_WIDTH, INVENTORY_HEIGHT)
        self.slots = 8  # Количество слотов в инвентаре
        self.slot_size = ITEM_SIZE
        self.slot_margin = 10
        
    def draw(self, surface, player_inventory):
        # Рисуем фон инвентаря
        pygame.draw.rect(surface, INVENTORY_COLOR, self.rect)
        
        # Рисуем слоты инвентаря
        for i in range(self.slots):
            slot_x = 20 + i * (self.slot_size + self.slot_margin)
            slot_rect = pygame.Rect(slot_x, 15, self.slot_size, self.slot_size)
            pygame.draw.rect(surface, (100, 100, 120), slot_rect, 2)
            
            # Рисуем предметы в инвентаре
            if i < len(player_inventory):
                item = player_inventory[i]
                # Создаем миниатюру предмета для инвентаря
                item_img = pygame.Surface((self.slot_size-4, self.slot_size-4))
                item_img.fill(item.image.get_at((0,0)))  # Берем цвет предмета
                surface.blit(item_img, (slot_x+2, 17))