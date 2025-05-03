import pygame
from constants import *
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.type = item_type
        self.world_size = (40, 40)  # Размер в игровом мире
        self.inventory_size = (40, 40)  # Размер в инвентаре
        
        # Создаем изображения
        self._create_images()
        
        # Начальная позиция и состояние
        self.image = self.world_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dragging = False
        self.drag_offset = (0, 0)
    
    def _create_images(self):
        """Создает изображения для мира и инвентаря"""
        colors = {
            "weapon": (255, 0, 0),
            "potion": (0, 255, 0),
            "scroll": (0, 0, 255),
            "food": (255, 255, 0)
        }
        color = colors.get(self.type, (200, 200, 200))
        
        # Изображение для игрового мира
        self.world_image = pygame.Surface(self.world_size)
        self.world_image.fill(color)
        
        # Изображение для инвентаря
        self.inventory_image = pygame.Surface(self.inventory_size)
        self.inventory_image.fill(color)
        pygame.draw.rect(self.inventory_image, (255,255,255), (0,0,*self.inventory_size), 2)  # Рамка для каждого предмета в инвентаре
    
    def start_drag(self, pos):
        self.dragging = True
        self.drag_offset = (self.rect.x - pos[0], self.rect.y - pos[1])
        self.image = self.inventory_image
        self.rect.size = self.inventory_size
    
    def update_drag(self, pos):
        if self.dragging:
            self.rect.x = pos[0] + self.drag_offset[0]
            self.rect.y = pos[1] + self.drag_offset[1]
    
    def stop_drag(self, world=False):
        self.dragging = False
        if world:
            self.image = self.world_image
            self.rect.size = self.world_size
        else:
            self.image = self.inventory_image
            self.rect.size = self.inventory_size