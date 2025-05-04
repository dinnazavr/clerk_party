import pygame
import random
from constants import *
from entities.player import Player
from entities.npc import NPC
from entities.item import Item
from ui.inventory import InventoryUI
from systems.dialogue import DialogueSystem


def generate_npcs(count, player):
    npcs = []
    occupied_areas = [player.rect.copy()]

    for i in range(count):
        attempts = 0
        placed = False

        while attempts < 1000 and not placed:
            x = random.randint(0, SCREEN_WIDTH - 30)
            y = random.randint(INVENTORY_HEIGHT + 10, SCREEN_HEIGHT - 50)
            new_rect = pygame.Rect(x, y, 30, 50)

            # Проверка коллизий
            collision = False
            for area in occupied_areas:
                if new_rect.colliderect(area.inflate(10, 10)):
                    collision = True
                    break

            if not collision:
                personality_id = (i % 16) + 1
                npc = NPC(x, y, i, personality_id)
                npcs.append(npc)
                occupied_areas.append(new_rect)
                placed = True

            attempts += 1

        if not placed:
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
                    personality_id = (i % 16) + 1
                    npc = NPC(corner[0], corner[1], i, personality_id)
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

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, selected_personality)
    npcs = generate_npcs(15, player)
    items = generate_items(5, player, npcs)

    # Группы спрайтов
    all_sprites = pygame.sprite.Group(player, *npcs, *items)
    npc_group = pygame.sprite.Group(*npcs)
    item_group = pygame.sprite.Group(*items)

    # Инициализация систем
    inventory_ui = InventoryUI(inventory_icon_rect.width)
    dialogue_system = DialogueSystem()

    # Состояния игры
    inventory_open = False
    running = True
    clock = pygame.time.Clock()
    conquered_npcs = []  # Храним id завоеванных NPC
    current_character = player  # Текущий управляемый персонаж
    controlled_npcs = {}  # Словарь управляемых NPC {id: character}

    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

                if event.key == pygame.K_i:
                    inventory_open = not inventory_open
                    inventory_ui.visible = inventory_open

                # Переключение между персонажами по Tab
                if event.key == pygame.K_TAB and len(conquered_npcs) > 0:
                    if current_character == player:
                        # Переключаемся на NPC
                        # Находим ближайшего завоеванного NPC, который еще не управляется
                        closest_npc = None
                        min_distance = float('inf')
                        
                        for npc in npcs:
                            if (npc.personality_id in conquered_npcs and 
                                npc.personality_id not in controlled_npcs):
                                
                                distance = (
                                    (player.rect.centerx - npc.rect.centerx)**2 + 
                                    (player.rect.centery - npc.rect.centery)**2
                                )**0.5
                                
                                if distance < min_distance:
                                    min_distance = distance
                                    closest_npc = npc
                        
                        if closest_npc:
                            # Создаем управляемого персонажа на основе NPC
                            npc_personality = next(
                                (p for p in dialogue_system.personalities 
                                if p["id"] == closest_npc.personality_id), None
                            )
                            
                            if npc_personality:
                                new_char = Player(
                                    closest_npc.rect.x,
                                    closest_npc.rect.y,
                                    npc_personality
                                )
                                new_char.inventory = player.inventory.copy()
                                controlled_npcs[closest_npc.personality_id] = new_char
                                all_sprites.add(new_char)
                                current_character = new_char
                    else:
                        # Возвращаемся к игроку
                        current_character = player

                # Взаимодействие только для основного персонажа
                if event.key == pygame.K_SPACE and current_character == player:
                    closest_npc = None
                    min_distance = DIALOGUE_RADIUS

                    # Ищем ближайшего NPC, который еще не завоеван
                    for npc in npcs:
                        if npc.personality_id in conquered_npcs:
                            continue

                        distance = (
                            (player.rect.centerx - npc.rect.centerx) ** 2
                            + (player.rect.centery - npc.rect.centery) ** 2
                        ) ** 0.5
                        if distance <= min_distance:
                            min_distance = distance
                            closest_npc = npc

                    if closest_npc and closest_npc.personality_id not in conquered_npcs:
                        if not dialogue_system.dialogue_visible:
                            dialogue_system.start_dialogue(closest_npc)
                            dialogue_system.start_guessing()
                        elif dialogue_system.guessing_mode:
                            if dialogue_system.check_guess():
                                conquered_id = closest_npc.personality_id
                                if conquered_id not in conquered_npcs:
                                    conquered_npcs.append(conquered_id)
                                    dialogue_system.close_dialogue()

            # Обработка кликов мыши
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if dialogue_system.guessing_mode:
                    dialogue_system.handle_guess_click(event.pos)
                elif inventory_icon_rect.collidepoint(event.pos):
                    inventory_open = not inventory_open
                    inventory_ui.visible = inventory_open

            # Обработка инвентаря
            if inventory_open:
                inventory_ui.handle_events(
                    event,
                    current_character.inventory,
                    current_character,
                    all_sprites,
                    npc_group,
                    item_group,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                )

        # Обновление текущего персонажа
        keys = pygame.key.get_pressed()
        current_character.update(keys)

        # Ограничение движения для всех управляемых персонажей
        for char in [player] + list(controlled_npcs.values()):
            if char.rect.top < INVENTORY_PANEL_HEIGHT:
                char.rect.top = INVENTORY_PANEL_HEIGHT

        # Проверка столкновений
        for npc in npcs:
            if current_character.rect.colliderect(npc.rect):
                current_character.rect.x = current_character.prev_x
                current_character.rect.y = current_character.prev_y

        # Сбор предметов
        collected_items = pygame.sprite.spritecollide(
            current_character, item_group, False
        )
        for item in collected_items:
            if not getattr(item, "dragging", False):
                current_character.collect_item(item)
                item.kill()

        # Проверка расстояния для автоматического закрытия диалога
        if dialogue_system.dialogue_visible and dialogue_system.current_npc:
            distance = (
                (
                    current_character.rect.centerx
                    - dialogue_system.current_npc.rect.centerx
                )
                ** 2
                + (
                    current_character.rect.centery
                    - dialogue_system.current_npc.rect.centery
                )
                ** 2
            ) ** 0.5
            if distance > DIALOGUE_RADIUS:
                dialogue_system.close_dialogue()

        # Отрисовка
        screen.fill(WHITE)

        # Рисуем игровой мир
        for sprite in all_sprites:
            if not (isinstance(sprite, Item) and getattr(sprite, "dragging", False)):
                screen.blit(sprite.image, sprite.rect)

        # Рисуем перетаскиваемый предмет
        if hasattr(inventory_ui, "dragged_item") and inventory_ui.dragged_item:
            dragged_item = inventory_ui.dragged_item
            dragged_item.rect.x = max(
                0, min(dragged_item.rect.x, SCREEN_WIDTH - dragged_item.rect.width)
            )
            dragged_item.rect.y = max(
                INVENTORY_PANEL_HEIGHT,
                min(dragged_item.rect.y, SCREEN_HEIGHT - dragged_item.rect.height),
            )
            screen.blit(dragged_item.image, dragged_item.rect)

        # Рисуем индикаторы взаимодействия
        for npc in npcs:
            distance = (
                (current_character.rect.centerx - npc.rect.centerx) ** 2
                + (current_character.rect.centery - npc.rect.centery) ** 2
            ) ** 0.5
            if distance <= DIALOGUE_RADIUS:
                if npc.personality_id in conquered_npcs:
                    # Индикатор для завоеванных NPC (синий с TAB)
                    pygame.draw.circle(
                        screen,
                        (100, 100, 255),
                        (npc.rect.centerx, npc.rect.top - 15),
                        8,
                    )
                    tab_text = font_small.render("TAB", True, WHITE)
                    screen.blit(
                        tab_text,
                        (
                            npc.rect.centerx - tab_text.get_width() // 2,
                            npc.rect.top - 30,
                        ),
                    )
                elif current_character == player and npc.personality_id not in conquered_npcs:
                    # Индикатор для новых NPC (зеленый)
                    pygame.draw.circle(
                        screen,
                        (100, 255, 100),
                        (npc.rect.centerx, npc.rect.top - 15),
                        8,
                    )

        # Рисуем интерфейс
        screen.blit(inventory_icon, inventory_icon_rect)
        if inventory_open:
            inventory_ui.draw(
                screen,
                current_character.inventory,
                inventory_icon_rect.right + 10,
                inventory_icon_rect.top,
            )

        # Рисуем диалоговую систему
        dialogue_system.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return "menu"