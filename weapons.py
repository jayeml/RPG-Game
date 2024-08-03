import math
import pygame
import random
from support import import_tilesheet, Cooldown, DeltaTime
from entity import Entity


class Weapon:
    def __init__(self, target_sprites, image, arms, bullet_image, damage, range, accuracy, bullet_speed, fire_rate, bullets_per_fire, piercing):
        self.images = image
        self.arm_images = arms
        self.bullet_images = bullet_image

        self.target_sprites = target_sprites

        self.damage = damage
        self.range = range
        self.accuracy = accuracy
        self.speed = bullet_speed
        self.fire_rate = Cooldown(fire_rate)
        self.bullets_per_fire = bullets_per_fire
        self.piercing = piercing

        self.projectiles = []

    def show_weapon(self, player_angle):
        current_image = self.images[player_angle]
        current_image_arms = self.arm_images[player_angle]

        weapon_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        weapon_surface.blit(current_image, (0, 0))
        weapon_surface.blit(current_image_arms, (0, 0))

        return weapon_surface

    def fire(self, pos, groups, obstacle_sprites, angle):
        if not self.fire_rate.on_cooldown:
            for _ in range(self.bullets_per_fire):
                self.projectiles.append(Projectile(pos, groups, obstacle_sprites, self.damage, self.range,
                                                   self.accuracy, angle, self.speed, self.bullet_images,
                                                   self.target_sprites, self.piercing))
            self.fire_rate.activate()

        self.fire_rate.update()


class RedTrombone(Weapon):
    def __init__(self, target_sprites):
        super().__init__(
            target_sprites,
            import_tilesheet(0, 0, 1, 8, 32, 'graphics\\tromone2.png'),
            import_tilesheet(0, 1, 1, 8, 32, 'graphics\\tromone2.png'),
            import_tilesheet(0, 0, 1, 4, 32, 'graphics\\bullets.png'),
            40,
            100,
            0,
            750,
            300,
            1,
            False
        )


class YellowTrombone(Weapon):
    def __init__(self, target_sprites):
        super().__init__(
            target_sprites,
            import_tilesheet(0, 0, 1, 8, 32, 'graphics\\trombone1.png'),
            import_tilesheet(0, 1, 1, 8, 32, 'graphics\\trombone1.png'),
            import_tilesheet(0, 1, 1, 4, 32, 'graphics\\bullets.png'),
            5,
            100,
            20,
            600,
            1000,
            10,
            True
        )


class Projectile(Entity):
    def __init__(self, pos, groups, passable_obstacle_sprites, damage, range, accuracy, angle, speed, images, target_sprites, piercing):
        super().__init__(pos, groups, passable_obstacle_sprites)
        self.damage = damage
        self.range = range
        self.angle = angle + math.radians((2 * random.random() - 1) * accuracy)
        self.speed = speed

        self.target_sprites = target_sprites

        self.hitbox.center = pos

        self.all_images = images
        self.image = images[0]

        self.hitbox = self.rect.inflate(-32, -32)
        self.piercing = piercing

        self.has_hit = []

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += math.cos(self.angle) * speed * DeltaTime.get_dt()
        self.hitbox.y += math.sin(self.angle) * speed * DeltaTime.get_dt()
        did_collide = self.collision()
        self.rect.center = self.hitbox.center
        if did_collide:
            self.kill()

    def animate(self):
        self.animation_frame += self.animation_speed * DeltaTime.get_dt()
        self.image = self.all_images[int(self.animation_frame % 4)]

    def collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                return True
        for sprite in self.target_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if not sprite.damage_cooldown.on_cooldown and sprite not in self.has_hit:
                    sprite.health -= self.damage
                    sprite.damage_cooldown.activate()
                    sprite.show_damage_cooldown.activate()
                    self.has_hit.append(sprite)
                if not self.piercing:
                    return True
        return False

    def update(self):
        self.animate()
        self.move(self.speed)


def init_weapons(sprite_group):
    rt = RedTrombone(sprite_group)
    yt = YellowTrombone(sprite_group)

    return rt, yt
