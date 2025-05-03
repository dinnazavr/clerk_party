import pygame
pygame.init()
pygame.font.init()
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

# Добавим константы для инвентаря
INVENTORY_HEIGHT = 80  # Высота панели инвентаря
INVENTORY_COLOR = (50, 50, 70)  # Цвет фона инвентаря
ITEM_SIZE = 40 # Размер предметов
INVENTORY_ITEM_SIZE = 40  # Размер предметов в инвентаре
INVENTORY_PANEL_HEIGHT = 50  # Высота панели инвентаря
