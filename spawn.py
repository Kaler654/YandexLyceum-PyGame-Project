import random as rand
import pygame
from enemy import Enemy
from vars import *


class SpawnEnemy:
    def __init__(self, spawn_points):
        """Стандартные настройки по умолчанию для спрайта"""
        self.spawn_points = spawn_points
        self.spawn_level = 1  # уровень создаваемого танка по умолчанию
        self.max_count_enemies = 5
        self.now = pygame.time.get_ticks()

    def level_up(self):
        """Повышение уровня противника в зависимости от этапа игры"""
        self.now = pygame.time.get_ticks()
        if self.now > 10000:
            self.spawn_level = 2
        if self.now > 20000:
            self.spawn_level = 3

    def spawn(self):
        """Создание танка если их кол-во меньше максимума"""
        if self.now > 120000:  # усложнение после 2-ух минут игры
            self.max_count_enemies = 10
        if len(enemies) < self.max_count_enemies:
            new_enemy = Enemy(*rand.choice(self.spawn_points), self.spawn_level)
            enemies.append(new_enemy)
