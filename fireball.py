import pygame as pg
import math
from settings import *


class FireBall(pg.sprite.Sprite):
    def __init__(self, mario, game):
        super().__init__()
        self.image = pg.image.load('images/FireMario/fireball.png').convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.mario = mario
        if self.mario.direction == RIGHT:
            self.angle = 30
            self.speed = FIREBALL_SPEED
            self.rect.left = self.mario.rect.right
        elif self.mario.direction == LEFT:
            self.angle = -30
            self.speed = -FIREBALL_SPEED
            self.rect.right = self.mario.rect.left
        self.rect.centery = self.mario.rect.centery
        self.pos = self.rect.center
        self.angle = math.radians(self.angle)
        self.game = game
        self.bounce = 1
        self.t = 0
        self.drop = 1

    def update(self):
        if self.rect.x > self.game.screen.get_rect().width or self.rect.x < 0 \
                or self.rect.y > self.game.screen.get_rect().height or self.rect.y < 0:
            self.kill()

        platform_hit = pg.sprite.spritecollide(self, self.game.bg.platform_group, False)
        if platform_hit:
            self.bounce = -self.bounce

        enemy = pg.sprite.spritecollideany(self, self.game.bg.enemies, False)
        if enemy:
            self.kill()
            enemy.kill()

        self.projectile_cal()

    def projectile_cal(self):
        self.t += 0.2
        x = self.pos[0] + self.speed * math.cos(self.angle) * self.t
        y = self.pos[1] + (-(self.speed * math.sin(self.angle) * self.t - (0.5 * 0.5 * self.t * self.t)) * self.bounce)
        self.pos = (x, y)
        self.rect.center = self.pos

    @staticmethod
    def change_angle(rad):

        return math.radians(-math.degrees(rad))

    def draw(self, win):
        win.blit(self.image, self.rect)