import random as rand
import pygame
from vars import *


class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        """Настройки по умолчанию для бонусов"""
        super().__init__(tiles_group, all_sprites)
        self.bonuses = ["shovel", "star", "grenade"]
        self.field = load_level(map_name)
        self.bonus = rand.choice(self.bonuses)
        self.random_x = rand.randint(0, width - 1)
        self.random_y = rand.randint(0, height - 1)
        self.find_pos()
        self.image = tile_images[self.bonus]
        self.rect = self.image.get_rect().move(
            tile_width * self.random_x, tile_height * self.random_y)
        self.tile_type = self.bonus

    def find_pos(self):
        """Нахождение свободной клетки для спавна бонуса"""
        tile = self.field[self.random_y][self.random_x]
        while tile != ".":
            self.random_x = rand.randint(0, width - 1)
            self.random_y = rand.randint(0, height - 1)
            tile = self.field[self.random_y][self.random_x]