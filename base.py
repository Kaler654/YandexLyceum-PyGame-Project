import pygame
from vars import *


class Base(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        """Стандартные настройки по умолчанию для спрайта"""
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.tile_type = tile_type
        self.game = True

    def game_over(self):
        """При попадании пули в базу - игра заканчивается"""
        self.game = False
        self.image = load_image("flag.png")
        screen.blit(load_image("empty.png"), (self.rect.x, self.rect.y))
        screen.blit(load_image("flag.png"), (self.rect.x, self.rect.y))
