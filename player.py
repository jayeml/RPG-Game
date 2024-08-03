import math
import pygame
from entity import Entity
from support import import_tilesheet, Cooldown, DeltaTime
from weapons import init_weapons


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, passable_obstacle_sprites, enemy_sprites):
        super().__init__(pos, groups, obstacle_sprites)

        self.groups = groups
        self.passable_obstacle_sprites = passable_obstacle_sprites

        self.hitbox = self.rect.inflate(-26, -26)
        self.status = 'idle'

        self.moving = False

        self.angle = 0
        self.angle_deg = 0
        self.sprite_direction = 0
        self.sprite_angles = [-180, -135, -90, -45, 0, 45, 90, 135, 180]

        self.bullet_start = [self.hitbox.bottomright, self.hitbox.midbottom, self.hitbox.bottomleft,
                             self.hitbox.midleft, self.hitbox.topleft, self.hitbox.midtop, self.hitbox.topright,
                             self.hitbox.midright]

        self.body_idle = import_tilesheet(0, 0, 1, 8, 32,
                                          'graphics\\idle.png')
        self.arms_idle = import_tilesheet(0, 0, 1, 8, 32,
                                          'graphics\\idlearms.png')

        self.body_walk = [
            import_tilesheet(0, 0, 1, 8, 32,
                             'graphics\\walk.png'),
            import_tilesheet(0, 1, 1, 8, 32,
                             'graphics\\walk.png'),
            import_tilesheet(0, 2, 1, 8, 32,
                             'graphics\\walk.png'),
        ]

        self.arms_walk = [
            import_tilesheet(0, 0, 1, 8, 32,
                             'graphics\\walkarms.png'),
            import_tilesheet(0, 1, 1, 8, 32,
                             'graphics\\walkarms.png'),
            import_tilesheet(0, 2, 1, 8, 32,
                             'graphics\\walkarms.png'),
        ]

        self.sprite_angle_indexes = {
            -180: 3,
            -135: 4,
            -90: 5,
            -45: 6,
            0: 7,
            45: 0,
            90: 1,
            135: 2,
            180: 3,
        }

        self.weapons = init_weapons(enemy_sprites)
        self.weapon_index = 0
        self.weapon_switch_cooldown = Cooldown(400)
        self.attacking = False

        body_surface = self.body_idle[self.sprite_direction]
        arm_surface = self.arms_idle[self.sprite_direction]

        self.image = pygame.Surface(body_surface.get_size(), pygame.SRCALPHA)

        self.image.blit(body_surface, (0, 0))
        self.image.blit(arm_surface, (0, 0))

        self.print_pos_cooldown = Cooldown(50)

        self.cooldowns = [self.weapon_switch_cooldown, self.print_pos_cooldown]

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if self.direction.x == self.direction.y == 0:
            self.moving = False
        else:
            self.moving = True

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if keys[pygame.K_LSHIFT] and not self.weapon_switch_cooldown.on_cooldown:
            self.attacking = not self.attacking
            self.weapon_switch_cooldown.activate()

        if keys[pygame.K_p] and not self.print_pos_cooldown.on_cooldown:
            self.print_pos_cooldown.activate()
            print(self.rect.center)

        mouse_press = pygame.mouse.get_pressed()

        if mouse_press[0] and self.attacking:
            self.weapons[self.weapon_index].fire(self.bullet_start[self.sprite_direction], self.groups, self.passable_obstacle_sprites, self.angle)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen_width, screen_height = pygame.display.get_window_size()

        center_x = screen_width / 2
        center_y = screen_height / 2

        dx = mouse_x - center_x
        dy = mouse_y - center_y

        self.angle = math.atan2(dy, dx)
        self.angle_deg = math.degrees(self.angle)

    def update_image(self):
        sprite_angle = min(self.sprite_angles, key=lambda x: abs(x - self.angle_deg))
        self.sprite_direction = self.sprite_angle_indexes[sprite_angle]
        if self.moving:
            self.animation_frame += self.animation_speed * DeltaTime.get_dt()
            body_surface = self.body_walk[int(self.animation_frame % 3)][self.sprite_direction]
            if not self.attacking:
                arm_surface = self.arms_walk[int(self.animation_frame % 3)][self.sprite_direction]
        else:
            body_surface = self.body_idle[self.sprite_direction]
            if not self.attacking:
                arm_surface = self.arms_idle[self.sprite_direction]

        if self.attacking:
            arm_surface = self.weapons[self.weapon_index].show_weapon(self.sprite_direction)

        self.image = pygame.Surface(body_surface.get_size(), pygame.SRCALPHA)

        self.image.blit(body_surface, (0, 0))
        self.image.blit(arm_surface, (0, 0))

        self.bullet_start = [self.hitbox.bottomright, self.hitbox.midbottom, self.hitbox.bottomleft,
                             self.hitbox.midleft, self.hitbox.topleft, self.hitbox.midtop, self.hitbox.topright,
                             self.hitbox.midright]

    def update(self):
        self.input()
        self.update_image()
        self.move(self.speed)
        self.update_hp()
        for cd in self.cooldowns:
            cd.update()

