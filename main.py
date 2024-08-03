import sys
import time
import pygame
from debug import show_text
from support import DeltaTime
from level import Level
from settings import *


class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('rpg game')

        self.previous_time = time.time()

        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEWHEEL:
                    self.level.scroll_wheel = event.y

            self.screen.fill('black')
            self.level.run()
            show_text(int(self.clock.get_fps()))
            pygame.display.update()
            DeltaTime.set_deltatime(self.clock.tick(FPS) / 1000)


if __name__ == '__main__':
    game = Game()
    game.run()
