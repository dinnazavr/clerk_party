import pygame
from constants import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, color_idx):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(COLORS[color_idx % len(COLORS)])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y