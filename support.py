import pygame


def import_tilesheet(x_offset, y_offset, n_rows, n_cols, size, path):
    tiles = []

    x_offset *= size
    y_offset *= size

    tile = pygame.image.load(path)

    for y in range(0, n_rows * size, size):
        for x in range(0, n_cols * size, size):
            tile_x_offset = x_offset + x
            tile_y_offset = y_offset + y
            image = pygame.Surface((size, size), pygame.SRCALPHA)
            image.blit(tile, (0, 0), (tile_x_offset, tile_y_offset, size, size))
            scaled_image = pygame.transform.scale(image, (64, 64))
            tiles.append(scaled_image)
    return tiles


class Cooldown:
    def __init__(self, length):
        self.length = length
        self.on_cooldown = False
        self.start_time = None

    def update(self):
        if self.on_cooldown:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.length:
                self.on_cooldown = False

    def activate(self):
        self.on_cooldown = True
        self.start_time = pygame.time.get_ticks()


class DeltaTime:
    dt = 1

    @classmethod
    def set_deltatime(cls, dt):
        cls.dt = dt

    @classmethod
    def get_dt(cls):
        return cls.dt

