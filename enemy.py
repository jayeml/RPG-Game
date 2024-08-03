import pygame

import debug
from entity import Entity
from support import import_tilesheet, DeltaTime


class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, health, images, player, layout):
        super().__init__(pos, groups, obstacle_sprites)
        self.health = health
        self.all_images = images
        self.all_damaged_images = self.create_damaged_sprites()
        self.image = self.all_images[0]

        self.hitbox = self.rect.inflate(-26, 0)
        self.player = player

        self.layout = layout

        self.speed = 50
        self.angle = 0
        self.direction = pygame.Vector2()
        self.pos = pygame.Vector2(self.rect.center)

    def set_direction(self):
        enemy_vec = pygame.Vector2(self.rect.center)
        player_vec = pygame.Vector2(self.player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            self.direction = (player_vec - enemy_vec).normalize()
        else:
            self.direction = pygame.Vector2()

    def animate(self):
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        if self.direction.x < 0:
            self.image.blit(self.all_images[0], (0, 0)) if not self.show_damage_cooldown.on_cooldown else self.image.blit(self.all_damaged_images[0], (0, 0))
        else:
            self.image.blit(self.all_images[1], (0, 0)) if not self.show_damage_cooldown.on_cooldown else self.image.blit(self.all_damaged_images[1], (0, 0))

    def move(self, speed):
        self.set_direction()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * speed * DeltaTime.get_dt()
        self.rect.center = self.pos
        self.hitbox.center = self.rect.center

    def create_damaged_sprites(self):
        damaged_images = []
        for i in self.all_images:
            i = i.copy()
            show_damage = pygame.Surface([1, 1], pygame.SRCALPHA, 32)
            show_damage.fill((255, 0, 0, 120))
            show_damage_converted = show_damage.convert_alpha()
            for x in range(0, i.width):
                for y in range(0, i.height):
                    _, _, _, alpha = i.get_at((x, y))
                    if alpha > 0:
                        i.blit(show_damage_converted, (x, y))
            damaged_images.append(i)
        return damaged_images

    def path_finding(self):
        p_row, p_col = self.player.get_layout_pos()
        self.layout[p_row][p_col] = 2

    def update(self):
        self.move(self.speed)
        self.update_hp()
        self.animate()


class Enemy1(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, player, layout):
        super().__init__(pos,
                         groups,
                         obstacle_sprites,
                         100,
                         import_tilesheet(0, 1, 1, 2, 32, 'graphics\\enemy1.png'),
                         player,
                         layout)
