import pygame
import random
from constants import *
from entities.player import Player
from entities.npc import NPC

def generate_npcs(count, player):
    npcs = []
    occupied_areas = [player.rect.copy()]  # Начинаем с области игрока

    for i in range(count):
        attempts = 0
        placed = False

        while attempts < 1000 and not placed:
            x = random.randint(0, SCREEN_WIDTH - 30)
            y = random.randint(0, SCREEN_HEIGHT - 50)
            new_rect = pygame.Rect(x, y, 30, 50)

            # Проверяем отступы от других объектов (минимум 5 пикселей)
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
                (10, 10),
                (SCREEN_WIDTH - 40, 10),
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

def game_loop(screen, selected_personality):
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    npcs = generate_npcs(15, player)

    all_sprites = pygame.sprite.Group(player, *npcs)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        player.update(keys)

        # Проверка столкновений с NPC
        for npc in npcs:
            if player.rect.colliderect(npc.rect):
                player.rect.x = player.prev_x
                player.rect.y = player.prev_y

        screen.fill(WHITE)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return "menu"