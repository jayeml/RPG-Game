import random
import pygame
import debug
from collections import Counter
from tile import Tile
from player import Player
from pytmx.util_pygame import load_pygame
from support import Cooldown
from enemy import Enemy1


class Level:
    def __init__(self):

        self.player = None
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.passable_obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.floor_sprites = YSortCameraGroup()

        self.debug_cooldown = Cooldown(100)
        self.debug_active = False

        self.scroll_wheel = 0

        self.layout = []
        self.enemy_poses = []

        self.create_map()

    def create_map(self):
        tmx_data = load_pygame('tiled_map\\tmx\\world map.tmx')

        for layer in tmx_data.visible_layers:
            if 'floor' not in layer.name and layer.name != 'elevation':
                for x, y, surf in layer.tiles():
                    if surf.get_height() > 64:
                        y -= 1
                    Tile((x * 64, y * 64), surf, self.visible_sprites)
            else:
                for x, y, surf in layer.tiles():
                    if surf.get_height() > 64:
                        y -= 1
                    Tile((x * 64, y * 64), surf, self.floor_sprites)
        hitboxes = tmx_data.get_layer_by_name('borderplayer')
        for x, y, surf in hitboxes.tiles():
            Tile((x * 64, y * 64), surf, self.obstacle_sprites)

        hitboxes2 = tmx_data.get_layer_by_name('borderall')
        for x, y, surf in hitboxes2.tiles():
            Tile((x * 64, y * 64), surf, self.passable_obstacle_sprites)

        for row in hitboxes.data:
            self.layout.append([0 if i == 0 else 1 for i in row])

        entity_locations = tmx_data.get_layer_by_name('entities').data
        for x in range(len(entity_locations[0])):
            for y in range(len(entity_locations)):
                if entity_locations[y][x] == 68:
                    self.player = Player((x * 64, y * 64), self.visible_sprites, self.obstacle_sprites,
                                         self.passable_obstacle_sprites, self.enemy_sprites)
                elif entity_locations[x][y] == 67:
                    self.enemy_poses.append((x, y))

        for x, y in self.enemy_poses:
            Enemy1((x * 64, y * 64), (self.visible_sprites, self.enemy_sprites), self.obstacle_sprites,
                   self.player, self.layout)

    def run(self):
        self.floor_sprites.custom_draw(self.player)
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.key_inputs()
        if self.debug_active:
            debug.show_direction(self.player)
            debug.show_hitboxes(self.obstacle_sprites, self.player)
            debug.show_hitboxes(self.enemy_sprites, self.player)

    def key_inputs(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_f] and not self.debug_cooldown.on_cooldown:
            self.debug_active = not self.debug_active
            self.debug_cooldown.activate()

        self.player.weapon_index = (self.scroll_wheel + self.player.weapon_index) % 2
        self.scroll_wheel = 0

        self.debug_cooldown.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            if -64 < offset_pos[0] < 768 or -64 < offset_pos[1] < 768:
                self.display_surface.blit(sprite.image, offset_pos)
