import pygame
import random
from constants import *
from entities.player import Player
from entities.npc import NPC
from entities.item import Item
from ui.inventory import InventoryUI

def generate_npcs(count, player):
    npcs = []
    occupied_areas = [player.rect.copy()]  # Начинаем с области игрока

    for i in range(count):
        attempts = 0
        placed = False

        while attempts < 1000 and not placed:
            x = random.randint(0, SCREEN_WIDTH - 30)
            y = random.randint(INVENTORY_HEIGHT + 10, SCREEN_HEIGHT - 50)  # Учитываем инвентарь
            new_rect = pygame.Rect(x, y, 30, 50)

            # Проверяем отступы от других объектов
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
                (10, INVENTORY_HEIGHT + 10),
                (SCREEN_WIDTH - 40, INVENTORY_HEIGHT + 10),
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

def generate_items(count, player, npcs):
    items = []
    occupied_areas = [player.rect.copy()]
    
    # Добавляем зону инвентаря как запретную зону
    inventory_area = pygame.Rect(0, 0, SCREEN_WIDTH, INVENTORY_HEIGHT)
    occupied_areas.append(inventory_area)
    
    # Добавляем NPC в занятые области
    for npc in npcs:
        occupied_areas.append(npc.rect)

    for i in range(count):
        attempts = 0
        placed = False
        item_type = random.choice(["weapon", "potion", "scroll", "food"])

        while attempts < 1000 and not placed:
            x = random.randint(0, SCREEN_WIDTH - ITEM_SIZE)
            y = random.randint(INVENTORY_HEIGHT + 10, SCREEN_HEIGHT - ITEM_SIZE)
            new_rect = pygame.Rect(x, y, ITEM_SIZE, ITEM_SIZE)

            # Проверяем отступы от других объектов
            collision = False
            for area in occupied_areas:
                if new_rect.colliderect(area.inflate(10, 10)):
                    collision = True
                    break

            if not collision:
                item = Item(x, y, item_type)
                items.append(item)
                occupied_areas.append(new_rect)
                placed = True

            attempts += 1

        if not placed:
            # Альтернативное размещение в углах, если не найдено место
            corners = [
                (10, INVENTORY_HEIGHT + 10),
                (SCREEN_WIDTH - ITEM_SIZE - 10, INVENTORY_HEIGHT + 10),
                (10, SCREEN_HEIGHT - ITEM_SIZE - 10),
                (SCREEN_WIDTH - ITEM_SIZE - 10, SCREEN_HEIGHT - ITEM_SIZE - 10),
            ]
            for corner in corners:
                corner_rect = pygame.Rect(corner[0], corner[1], ITEM_SIZE, ITEM_SIZE)
                collision = False
                for area in occupied_areas:
                    if corner_rect.colliderect(area.inflate(10, 10)):
                        collision = True
                        break
                if not collision:
                    item = Item(corner[0], corner[1], item_type)
                    items.append(item)
                    occupied_areas.append(corner_rect)
                    placed = True
                    break

    return items

def game_loop(screen, selected_personality):
    # Инициализация интерфейса инвентаря
    inventory_ui = InventoryUI()
    
    # Создание игрока
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # Генерация NPC и предметов
    npcs = generate_npcs(15, player)
    items = generate_items(5, player, npcs)
    
    # Группы спрайтов
    all_sprites = pygame.sprite.Group(player, *npcs, *items)
    npc_group = pygame.sprite.Group(*npcs)
    item_group = pygame.sprite.Group(*items)
    
    clock = pygame.time.Clock()
    running = True

    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Обновление игрока
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Проверка столкновений с NPC
        for npc in npcs:
            if player.rect.colliderect(npc.rect):
                player.rect.x = player.prev_x
                player.rect.y = player.prev_y

        # Проверка сбора предметов
        collected_items = pygame.sprite.spritecollide(player, item_group, True)
        for item in collected_items:
            player.collect_item(item)

        # Отрисовка
        screen.fill(WHITE)
        
        # Рисуем игровые объекты
        all_sprites.draw(screen)
        
        # Рисуем инвентарь поверх всего
        inventory_ui.draw(screen, player.inventory)

        pygame.display.flip()
        clock.tick(60)

    return "menu"