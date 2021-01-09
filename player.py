import pygame
from pygame.locals import *
from vars import *
from tile import Tile


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, health, speed):
        """Стандартные настройки по умолчанию для спрайта"""
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x, self.y = pos_x, pos_y
        self.angle = 0
        self.top = self.down = self.left = self.right = False
        self.last_direction = "top"
        self.tile_type = "player"
        self.hp = health
        self.speed = speed
        self.damage = 5
        self.died = False
        self.kills = 0
        self.shoot_delay = 500

    def get_position(self):
        """Функция возвращает координаты игрока"""
        return self.rect.x, self.rect.y

    def move(self):
        """Движение в зависимости от того, какая клавиша зажата"""
        if self.left:
            self.rotate_player("left")
            self.rect.x -= self.speed
        elif self.right:
            self.rotate_player("right")
            self.rect.x += self.speed
        elif self.top:
            self.rotate_player("top")
            self.rect.y -= self.speed
        elif self.down:
            self.rotate_player("down")
            self.rect.y += self.speed

    def rotate_player(self, side):
        """Поворот игрока, реализовано так: игрок поворачивается сначала до того момента,
        пока не будет в положении по умолчанию, далее следует поворот на нужное кол-во градусов"""
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.angle = 0
        if side == "left":
            self.image = pygame.transform.rotate(self.image, 90)
            self.angle += 90
        elif side == "right":
            self.image = pygame.transform.rotate(self.image, 270)
            self.angle += 270
        elif side == "top":
            pass
        elif side == "down":
            self.image = pygame.transform.rotate(self.image, 180)
            self.angle += 180
        self.last_direction = side

    def check_position(self):
        """Проверка выходит ли игрок за пределы поля"""
        if self.rect.x < 0:
            self.left = False
            self.rect.x += 1
        elif self.rect.x + 20 > 499:
            self.right = False
            self.rect.x -= 1
        elif self.rect.y < 0:
            self.top = False
            self.rect.y += 1
        elif self.rect.y + 20 > 499:
            self.down = False
            self.rect.y -= 1

    def check_collision(self):
        """Проверка - касается ли хитбокс игрока чего-либо, если да, то блокировка движения"""
        for sprite in all_sprites:
            if pygame.Rect.colliderect(self.rect, sprite.rect) and sprite.tile_type in \
                    ("wall", "iron-wall", "water", "base", "grenade", "shovel", "star", "enemy"):
                if sprite.tile_type in ("grenade", "shovel", "star"):
                    bonus.play()
                    if sprite.tile_type == "grenade":
                        for enemy in enemies:
                            enemy.death(999)
                    elif sprite.tile_type == "star":
                        self.hp += 15
                        self.shoot_delay = 250
                        self.damage = 10
                    elif sprite.tile_type == "shovel":
                        level = load_level(map_name)
                        for _ in range(0, len(level)):
                            if "!" in list(level[_]):
                                index_base = list(level[_]).index("!")
                                x, y = _, index_base
                        for j in range(y - 2, y + 3):
                            for i in range(x - 2, x + 3):
                                if (x, y) != (i, j):
                                    Tile('iron-wall', j, i)
                    sprite.kill()
                    return
                if sprite.tile_type == "enemy":
                    return
                if self.last_direction == "left":
                    self.rect.x += 1
                elif self.last_direction == "right":
                    self.rect.x -= 1
                elif self.last_direction == "top":
                    self.rect.y += 1
                elif self.last_direction == "down":
                    self.rect.y -= 1

    def death(self, damage):
        """Уменьшение жизней игрока при попадании по нему"""
        self.hp -= damage
        if self.hp <= 0:
            self.died = True

    def freeze(self):
        """Обездвиживает игрока"""
        self.top = self.down = self.left = self.right = False

    def update(self, *args):
        """Движение игрока по нажатию клавиш"""
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if pygame.key.get_pressed()[K_UP]:
            self.top = True
            self.down = self.left = self.right = False
        else:
            self.top = False

        if pygame.key.get_pressed()[K_DOWN]:
            self.down = True
            self.top = self.left = self.right = False
        else:
            self.down = False

        if pygame.key.get_pressed()[K_LEFT]:
            self.left = True
            self.top = self.down = self.right = False
        else:
            self.left = False

        if pygame.key.get_pressed()[K_RIGHT]:
            self.right = True
            self.top = self.down = self.left = False
        else:
            self.right = False

        self.check_position()
        self.check_collision()
        self.move()
