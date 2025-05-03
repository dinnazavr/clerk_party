import pygame
from constants import *
from entities.item import Item

class InventoryUI:
    def __init__(self, icon_width):
        self.height = 40
        self.bg_color = (70, 70, 90, 200)
        self.surface = pygame.Surface((SCREEN_WIDTH //5, self.height), pygame.SRCALPHA)
        self.dragged_item = None
        self.visible = False
    
    def handle_events(self, event, player_inventory, player, all_sprites, npc_group, item_group, screen_width, screen_height):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for item in player_inventory:
                if item.rect.collidepoint(event.pos):
                    self.dragged_item = item
                    item.start_drag(event.pos)
                    return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragged_item:
            # Проверяем границы экрана
            if (0 <= event.pos[0] <= screen_width - self.dragged_item.rect.width and
                INVENTORY_PANEL_HEIGHT <= event.pos[1] <= screen_height - self.dragged_item.rect.height):
                
                # Проверяем коллизии
                temp_rect = pygame.Rect(event.pos[0], event.pos[1], 
                                    self.dragged_item.rect.width,
                                    self.dragged_item.rect.height)
                
                collision = False
                for npc in npc_group:
                    if npc.rect.colliderect(temp_rect):
                        collision = True
                        break
                
                if not collision and not player.rect.colliderect(temp_rect):
                    # Создаем новый предмет в мире
                    new_item = Item(event.pos[0], event.pos[1], self.dragged_item.type)
                    all_sprites.add(new_item)
                    item_group.add(new_item)
                    
                    # Удаляем из инвентаря
                    player_inventory.remove(self.dragged_item)
            
            # Сбрасываем перетаскивание
            self.dragged_item.stop_drag()
            self.dragged_item = None
            return True
        
        elif event.type == pygame.MOUSEMOTION and self.dragged_item:
            self.dragged_item.update_drag(event.pos)
            return True
        
        return False
    
    def _try_place_item(self, player_inventory, all_sprites, item_group, npc_group, player):
        """Пытается разместить предмет в мире, возвращает True если успешно"""
        item = self.dragged_item
        mouse_pos = pygame.mouse.get_pos()
        
        # Проверяем валидность позиции
        if (mouse_pos[1] <= INVENTORY_PANEL_HEIGHT or  # Над инвентарем
            any(npc.rect.collidepoint(mouse_pos) for npc in npc_group) or  # На NPC
            player.rect.collidepoint(mouse_pos)):  # На игроке
            item.stop_drag(world=False)
            return False
        
        # Проверяем коллизии с другими предметами
        temp_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], *item.world_size)
        if any(i.rect.colliderect(temp_rect) for i in item_group if i != item):
            item.stop_drag(world=False)
            return False
        
        # Успешное размещение в мире
        new_item = Item(mouse_pos[0], mouse_pos[1], item.type)
        all_sprites.add(new_item)
        item_group.add(new_item)
        
        # Удаляем из инвентаря
        player_inventory.remove(item)
        return True
    
    def draw(self, screen, player_inventory, x_pos, y_pos):
        if not self.visible:
            return

        # Фон инвентаря
        self.surface.fill(self.bg_color)
        screen.blit(self.surface, (x_pos, y_pos))
        
        # Рисуем предметы
        for i, item in enumerate(player_inventory):
            if item == self.dragged_item:
                continue
                
            item_x = x_pos + 10 + i * (INVENTORY_ITEM_SIZE + 5)
            item.rect.x = item_x
            item.rect.y = y_pos + (self.height - INVENTORY_ITEM_SIZE) // 2
            screen.blit(item.inventory_image, item.rect)