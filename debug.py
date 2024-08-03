import pygame
from math import sin, cos

pygame.init()
font = pygame.font.Font(None, 30)


def show_text(info, y=10, x=10):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surf, debug_rect)


def show_direction(player):
    display_surface = pygame.display.get_surface()
    half_width = display_surface.get_size()[0] // 2
    half_height = display_surface.get_size()[1] // 2
    pygame.draw.line(display_surface, (255, 255, 255), (half_width, half_height), (
        half_width + (100 * cos(player.angle)), half_height + (100 * sin(player.angle))))


def show_hitboxes(sprites, player):
    display_surface = pygame.display.get_surface()
    half_width = display_surface.get_size()[0] // 2
    half_height = display_surface.get_size()[1] // 2
    offset = pygame.math.Vector2()

    offset.x = player.hitbox.centerx - half_width
    offset.y = player.hitbox.centery - half_height

    for sprite in sprites:
        offset_pos = sprite.hitbox.topleft - offset
        pygame.draw.rect(display_surface, 'black', (offset_pos[0], offset_pos[1], sprite.hitbox.width, sprite.hitbox.height), 1)
