import pygame
from vars import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, owner):
        """Стандартные настройки по умолчанию для спрайта"""
        super().__init__(tiles_group, all_sprites)
        self.image = bullet_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.direction = direction
        self.angle = 0
        self.tile_type = "empty"
        self.owner = owner
        self.last_direction = None

    def rotate_bullet(self, side):
        """Поворот пули в нужную сторону"""
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

    def check_collision(self):
        """Проверка касается ли пуля чего-либо
        Если да, то уничтожение пули и нанесение урона объекту"""
        for sprite in all_sprites:
            if pygame.Rect.colliderect(self.rect, sprite.rect) and sprite.tile_type in \
                    ("wall", "iron-wall", "player", "enemy", "base"):
                if self.owner.tile_type == "player" and sprite.tile_type == "iron-wall":
                    iron.play()
                if self.owner.tile_type == "player" and sprite.tile_type == "wall":
                    wall.play()
                if sprite.tile_type in ("wall", "player", "enemy", "base"):  #
                    if sprite.tile_type == "player" and self.owner.tile_type == "enemy":
                        sprite.death(self.owner.damage)
                    elif sprite.tile_type == "enemy" and self.owner.tile_type == "player":
                        hit.play()
                        flag = sprite.death(self.owner.damage)
                        if flag:
                            self.owner.kills += 1
                    elif sprite.tile_type == "base":
                        sprite.game_over()
                    elif sprite.tile_type == "wall":
                        self.sprite_kill(sprite)
                    else:
                        return

                self.kill()
        if not pygame.Rect(0, 0, 500, 500).contains(self.rect):
            iron.play()
            self.kill()

    def sprite_kill(self, sprite):
        """Уничтожение спрайта при попадании"""
        sprite.tile_type = "empty"
        sprite.image = load_image("empty.png")

    def update(self):
        """Обновление координат при полете пули"""
        if self.direction == "left":
            self.rotate_bullet("left")
            self.rect.x -= 2
        elif self.direction == "right":
            self.rotate_bullet("right")
            self.rect.x += 2
        elif self.direction == "top":
            self.rotate_bullet("top")
            self.rect.y -= 2
        elif self.direction == "down":
            self.rotate_bullet("down")
            self.rect.y += 2
        self.check_collision()
        screen.blit(self.image, (self.rect.x, self.rect.y))


