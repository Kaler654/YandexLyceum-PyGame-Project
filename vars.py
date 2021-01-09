import os
import sys
import random as rand
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


pygame.init()
pygame.display.set_caption('Battle City')
size = (725, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
volume1 = 0.2
volume2 = 0.1
game_start = pygame.mixer.Sound("sounds/gamestart.ogg")
game_start.set_volume(volume1)
fire = pygame.mixer.Sound("sounds/fire.ogg")
fire.set_volume(volume1)
iron = pygame.mixer.Sound("sounds/iron.ogg")
iron.set_volume(volume1)
hit = pygame.mixer.Sound("sounds/hit.ogg")
hit.set_volume(volume1)
wall = pygame.mixer.Sound("sounds/wall.ogg")
wall.set_volume(volume1)
bg = pygame.mixer.Sound("sounds/background.ogg")
bg.set_volume(volume2)
bonus = pygame.mixer.Sound("sounds/bonus.ogg")
bonus.set_volume(volume1)
gameover = pygame.mixer.Sound("sounds/gameover.ogg")
gameover.set_volume(volume1)
sounds = [game_start, fire, iron, hit, wall, bg, bonus, gameover]
FPS = 60
width = height = 25
player = None
enemies = []
spawn_points = []
bonuses = []
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('empty.png'),
    'iron-wall': load_image('iron-wall.png'),
    'water': load_image('water.png'),
    'base': load_image('base.png'),
    'star': load_image('star.png'),
    'grenade': load_image('grenade.png'),
    'shovel': load_image('shovel.png')
}
player_image = load_image('player.png')
enemy_image = load_image("enemy1.png")
bullet_image = load_image('bullet.png')
map_name = rand.choice(("map1.txt", "map2.txt", "map3.txt"))

tile_width = tile_height = 20
