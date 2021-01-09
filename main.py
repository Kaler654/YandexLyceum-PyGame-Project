import sys
import time
import pygame
from bullet import Bullet
from field import Field
from player import Player
from tile import Tile
from spawn import SpawnEnemy
from base import Base
from bonus import Bonus
from vars import *


def terminate():
    """Прекращение работы программы"""
    pygame.quit()
    sys.exit()


def start_screen():
    """Запуск стартового экрана игры"""
    pygame.display.set_icon(player_image)
    background = pygame.transform.scale(load_image('empty.png'), (width, height))
    screen.blit(background, (0, 0))
    font = pygame.font.Font("fonts/prstart.ttf", 56)
    screen.blit(font.render("BATTLE", True, pygame.Color('white')), [190, 35])
    screen.blit(font.render("CITY", True, pygame.Color('white')), [240, 115])
    font = pygame.font.Font("fonts/prstart.ttf", 16)
    screen.blit(font.render("PRESS ENTER", True, pygame.Color('white')), [265, 280])
    screen.blit(font.render("TO START PLAYING", True, pygame.Color('white')), [225, 310])
    count = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game()
                    return
        if count == 0:
            screen.blit(font.render("PRESS ENTER", True, pygame.Color('black')), [265, 280])
            screen.blit(font.render("TO START PLAYING", True, pygame.Color('black')), [225, 310])
            count = 1
        else:
            screen.blit(font.render("PRESS ENTER", True, pygame.Color('white')), [265, 280])
            screen.blit(font.render("TO START PLAYING", True, pygame.Color('white')), [225, 310])
            count = 0
        pygame.display.flip()
        clock.tick(3)


def end_screen(flag):
    """Запуск конечной заставки в зависимости от результата"""
    if flag:
        first_word = "YOU"
        second_word = "WIN"
    else:
        first_word = "GAME"
        second_word = "OVER"
    game_start.stop()
    bg.stop()
    gameover.play()
    surface = pygame.Surface((725, 500))
    font = pygame.font.Font("fonts/prstart.ttf", 56)
    surface.blit(font.render(first_word, True, pygame.Color('white')), [240, 150])
    surface.blit(font.render(second_word, True, pygame.Color('white')), [240, 230])
    time.sleep(3)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(surface, (0, 0))
        pygame.display.flip()


def statistic(hp, kills, damage, shoot_delay):
    """Вывод статистики"""
    surface = pygame.Surface((225, 500))
    surface.fill((179, 179, 179))
    screen.blit(surface, (500, 0))
    font = pygame.font.Font(None, 25)
    color = (0, 0, 128)
    if kills >= 50:
        end_screen(True)
    health = font.render(f"Здоровье игрока: {hp}", True, color)
    kills = font.render(f"Кол-во убитых: {kills}", True, color)
    damage = font.render(f"Урон: {damage}", True, color)
    shoot_delay = font.render(f"Задержка выстрела: {shoot_delay}", True, color)
    screen.blits(((health, (505, 10)),
                  (kills, (505, 40)), (damage, (505, 70)), (shoot_delay, (505, 100))))


def generate_level(level):
    """Генерация уровня по файлу"""
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '$':
                Tile('iron-wall', x, y)
            elif level[y][x] == '!':
                base = Base('base', x, y)
            elif level[y][x] == '%':
                Tile('water', x, y)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                spawn_points.append((x, y))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y, 40, 1)
    return base, new_player, x, y


def start_game():
    """Запуск игры"""
    game_start.play()
    base, player, level_x, level_y = generate_level(load_level(map_name))
    pygame.time.set_timer(pygame.USEREVENT, 2000)
    enemy_shoot = pygame.USEREVENT + 0
    spawn_enemies = pygame.USEREVENT + 1
    random_rotate_enemies = pygame.USEREVENT + 2
    spawn_bonus = pygame.USEREVENT + 3
    bg_music_on = pygame.USEREVENT + 4
    pygame.time.set_timer(enemy_shoot, 2000)
    pygame.time.set_timer(spawn_enemies, 4000)
    pygame.time.set_timer(random_rotate_enemies, 5000)
    pygame.time.set_timer(spawn_bonus, 20000)
    pygame.time.set_timer(bg_music_on, 4200, True)
    spawn_enemy = SpawnEnemy(spawn_points)
    field = Field(width, height)
    field.render(player, screen)
    last_shoot = 0
    volume1 = 0.2
    volume2 = 0.1

    while True:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if now - last_shoot > player.shoot_delay:
                        last_shoot = now
                        x, y = player.get_position()
                        fire.play()
                        bullet = Bullet(x, y, player.last_direction, player)
                elif event.key == 61:
                    volume1 += 0.1
                    volume2 += 0.1
                    for sound in sounds:
                        if sound != bg:
                            sound.set_volume(volume1)
                        else:
                            sound.set_volume(volume2)
                elif event.key == 45:
                    volume1 -= 0.1
                    volume2 -= 0.1
                    for sound in sounds:
                        if sound != bg:
                            sound.set_volume(volume1)
                        else:
                            sound.set_volume(volume2)
            elif event.type == enemy_shoot:
                for enemy in enemies:
                    if not enemy.died:
                        x, y = enemy.get_position()
                        bullet = Bullet(x, y, enemy.last_direction, enemy)
                    else:
                        enemies.remove(enemy)
            elif event.type == spawn_enemies:
                spawn_enemy.spawn()
            elif event.type == random_rotate_enemies:
                for enemy in enemies:
                    enemy.collision = True
            elif event.type == spawn_bonus:
                if len(bonuses) != 0:
                    bonuses[0].kill()
                    bonuses.clear()
                bonus = Bonus()
                bonuses.append(bonus)
            elif event.type == bg_music_on:
                bg.play(-1)
        statistic(player.hp, player.kills, player.damage, player.shoot_delay)
        spawn_enemy.level_up()
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
        if now > 300000:
            end_screen(True)
        if player.died or not base.game:
            player.freeze()
            end_screen(False)


start_screen()
