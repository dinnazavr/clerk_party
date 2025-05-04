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
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0) 
RED = (255, 0, 0)   
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

DIALOGUE_RADIUS = 55  # Радиус взаимодействия с NPC
DIALOGUE_BG_COLOR = (40, 40, 50, 220)  # Цвет фона диалога
DIALOGUE_TEXT_COLOR = (255, 255, 255)  # Цвет текста
DEBUG_MODE = False  # Для отображения зон взаимодействия