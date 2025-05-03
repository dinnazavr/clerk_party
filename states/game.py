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
            y = random.randint(
                INVENTORY_HEIGHT + 10, SCREEN_HEIGHT - 50
            )  # Учитываем инвентарь
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
    occupied_areas = [
        player.rect.copy(),
        pygame.Rect(0, 0, SCREEN_WIDTH, INVENTORY_HEIGHT),
    ]

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
    # Загрузка иконки инвентаря
    try:
        inventory_icon = pygame.image.load("images/inventory_icon.png").convert_alpha()
        inventory_icon = pygame.transform.scale(inventory_icon, (40, 40))
    except:
        inventory_icon = pygame.Surface((40, 40))
        inventory_icon.fill((150, 150, 200))

    inventory_icon_rect = inventory_icon.get_rect(topleft=(10, 10))

    # Инициализация игровых объектов
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    npcs = generate_npcs(15, player)
    items = generate_items(5, player, npcs)

    # Группы спрайтов
    all_sprites = pygame.sprite.Group(player, *npcs, *items)
    npc_group = pygame.sprite.Group(*npcs)
    item_group = pygame.sprite.Group(*items)

    # Инициализация инвентаря
    inventory_ui = InventoryUI(inventory_icon_rect.width)
    inventory_open = False

    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_i:
                    inventory_open = not inventory_open
                    inventory_ui.visible = inventory_open
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
                    # Проверяем клик именно по иконке инвентаря
                    if inventory_icon_rect.collidepoint(event.pos):
                        inventory_open = not inventory_open
                        inventory_ui.visible = inventory_open
            
            # Обработка перетаскивания только при открытом инвентаре
            if inventory_open:
                handled = inventory_ui.handle_events(
                    event, 
                    player.inventory, 
                    player, 
                    all_sprites,
                    npc_group,
                    item_group,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                )
                if handled:
                    continue

        # Обновление игрока
        keys = pygame.key.get_pressed()
        player.update(keys)
        if player.rect.top < INVENTORY_PANEL_HEIGHT:
            player.rect.top = INVENTORY_PANEL_HEIGHT

        # Проверка столкновений с NPC
        for npc in npcs:
            if player.rect.colliderect(npc.rect):
                player.rect.x = player.prev_x
                player.rect.y = player.prev_y

        # Сбор предметов (кроме перетаскиваемых)
        collected_items = pygame.sprite.spritecollide(player, item_group, False)
        for item in collected_items:
            if not getattr(item, 'dragging', False):
                player.collect_item(item)
                item.kill()

        # Отрисовка
        screen.fill(WHITE)
        
        # Рисуем игровые объекты (кроме перетаскиваемого)
        for sprite in all_sprites:
            if not (isinstance(sprite, Item) and getattr(sprite, 'dragging', False)):
                screen.blit(sprite.image, sprite.rect)
        
        # Рисуем перетаскиваемый предмет с проверкой границ
        if hasattr(inventory_ui, 'dragged_item') and inventory_ui.dragged_item:
            dragged_item = inventory_ui.dragged_item
            dragged_item.rect.x = max(0, min(dragged_item.rect.x, SCREEN_WIDTH - dragged_item.rect.width))
            dragged_item.rect.y = max(INVENTORY_PANEL_HEIGHT, min(dragged_item.rect.y, SCREEN_HEIGHT - dragged_item.rect.height))
            screen.blit(dragged_item.image, dragged_item.rect)
        
        # Рисуем интерфейс
        screen.blit(inventory_icon, inventory_icon_rect)
        if inventory_open:
            inventory_ui.draw(screen, player.inventory, inventory_icon_rect.right + 10, inventory_icon_rect.top)

        pygame.display.flip()
        clock.tick(60)

    return "menu"