import random as rand
import pygame
from vars import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, level):
        """Стандартные настройки по умолчанию для спрайта"""
        super().__init__(enemy_group, all_sprites)
        # значения по умолчанию
        self.speed = 1
        self.damage = 5
        self.hp = 5
        self.image = enemy_image
        self.x, self.y = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.angle = 0
        self.top = self.left = self.right = False
        self.down = True
        self.died = False
        self.last_direction = "down"
        self.tile_type = "enemy"
        self.collision = False
        self.level = level
        self.set_options()

    def set_options(self):
        """Установка параметров и изображения в зависимости от уровня"""
        if self.level == 2:
            self.image = load_image("enemy2.png")
            self.hp = 10
            self.damage = 10
            self.level = 2
        elif self.level == 3:
            self.image = load_image("enemy3.png")
            self.hp = 15
            self.damage = 15
            self.level = 3

    def get_position(self):
        """Функция возвращает координаты противника"""
        return self.rect.x, self.rect.y

    def move(self):
        """Движение в зависимости от того, какая сторона выбрана"""
        if self.left:
            self.rotate_enemy("left")
            self.rect.x -= self.speed
        elif self.right:
            self.rotate_enemy("right")
            self.rect.x += self.speed
        elif self.top:
            self.rotate_enemy("top")
            self.rect.y -= self.speed
        elif self.down:
            self.rotate_enemy("down")
            self.rect.y += self.speed

    def rotate_enemy(self, side):
        """Поворот противника, реализовано так: игрок поворачивается сначала до того момента,
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
        """Проверка выходит ли противник за пределы поля"""
        if self.rect.x + 1 <= 0:
            self.left = False
            self.collision = True
        elif self.rect.x + 19 >= 499:
            self.right = False
            self.collision = True
        elif self.rect.y + 1 <= 0:
            self.top = False
            self.collision = True
        elif self.rect.y - 1 + 20 >= 499:
            self.down = False
            self.collision = True

    def check_collision(self):
        """Проверка - касается ли хитбокс проивника чего-либо, если да, то разворот в рандомную
        сторону"""
        for sprite in all_sprites:
            if pygame.Rect.colliderect(self.rect, sprite.rect) and sprite.tile_type in \
                    ("wall", "iron-wall", "water", "base", "grenade", "shovel", "star",
                     "player") or self.collision:
                if sprite.tile_type in ("grenade", "shovel", "star"):
                    return
                if sprite.tile_type == "player":
                    return
                if self.last_direction == "left":
                    self.rect.x += 1
                    self.left = False
                elif self.last_direction == "right":
                    self.rect.x -= 1
                    self.right = False
                elif self.last_direction == "top":
                    self.rect.y += 1
                    self.top = False
                elif self.last_direction == "down":
                    self.rect.y -= 1
                    self.down = False
                self.collision = False
                return True
        return False

    def death(self, damage):
        """Уменьшение жизней противника при попадании по нему"""
        self.hp -= damage
        if self.hp <= 0:
            self.died = True
            self.kill()
            self.image = load_image("empty.png")
            self.tile_type = "empty"
            return True
        return False

    def update(self, *args):
        """Рандомное движение противника"""
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.check_position()
        if self.check_collision():
            directions = ["left", "right", "top", "down"]
            if self.last_direction == "left":
                directions.remove("left")
            elif self.last_direction == "right":
                directions.remove("right")
            elif self.last_direction == "top":
                directions.remove("top")
            else:
                directions.remove("down")
            rand.shuffle(directions)
            if directions[0] == "left":
                self.left = True
            elif directions[0] == "right":
                self.right = True
            elif directions[0] == "top":
                self.top = True
            else:
                self.down = True
        self.move()
