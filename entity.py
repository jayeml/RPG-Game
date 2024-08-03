import pygame
from support import Cooldown, DeltaTime
from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect

        self.direction = pygame.math.Vector2()
        self.speed = 400

        self.animation_speed = 10
        self.animation_frame = 0

        self.health = 100
        self.pos = pygame.Vector2(self.rect.center)

        self.damage_cooldown = Cooldown(10)
        self.show_damage_cooldown = Cooldown(120)

        self.obstacle_sprites = obstacle_sprites

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * speed * DeltaTime.get_dt()
        self.hitbox.centerx = self.pos.x
        self.collision('horizontal')

        self.pos.y += self.direction.y * speed * DeltaTime.get_dt()
        self.hitbox.centery = self.pos.y
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.pos.x = self.hitbox.centerx
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.pos.x = self.hitbox.centerx

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.pos.y = self.hitbox.centery
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.pos.y = self.hitbox.centery

    def get_layout_pos(self):
        row = int(self.rect.centerx / TILESIZE)
        col = int(self.rect.centery / TILESIZE)
        return row, col

    def update_hp(self):
        self.show_damage_cooldown.update()
        self.damage_cooldown.update()
        if self.health <= 0:
            self.kill()

    def update(self):
        self.update_hp()
        self.move(self.speed)
