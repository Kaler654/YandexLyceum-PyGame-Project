from vars import *


class Field:
    # создание поля
    def __init__(self, width, height):
        """Настройки по умолчанию для поля"""
        self.width = width
        self.height = height
        self.board = load_level(map_name)
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 20

    def render(self, player, screen):
        """Отображение каждой клетки"""
        left = self.left
        top = self.top
        for height in self.board:
            for width in height:
                if width == ".":
                    screen.blit(tile_images["empty"], (left, top))
                elif width == "#":
                    screen.blit(tile_images["wall"], (left, top))
                elif width == "$":
                    screen.blit(tile_images["iron-wall"], (left, top))
                elif width == "%":
                    screen.blit(tile_images["water"], (left, top))
                elif width == "&":
                    screen.blit(enemy_image, (left, top))
                elif width == "g":
                    screen.blit(tile_images["grenade"], (left, top))
                elif width == "s":
                    screen.blit(tile_images["star"], (left, top))
                elif width == "l":
                    screen.blit(tile_images["shovel"], (left, top))
                elif width == "@":
                    self.player_left, self.player_top = left, top
                left += self.cell_size
            top += self.cell_size
            left = self.left
