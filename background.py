import pygame as pg
import sys
from settings import *
import os
from stats import Stats

__all__ = ['Background']


class Background:
    def __init__(self, mario, game, screen, level):
        self.bg = []
        for i in range(1, 9):
            self.bg.append(pg.image.load('images/bg/bg-{}.jpg'.format(str(i))))

        for i in range(len(self.bg)):
            self.bg[i] = pg.transform.scale(self.bg[i],
                                                (int(self.bg[i].get_rect().width * BG_SCALER),
                                                 int(self.bg[i].get_rect().height * BG_SCALER)))
        self.mario = mario
        self.coins = 0
        self.background = self.bg[0]
        self.screen = screen
        self.game = game
        self.background_rect = self.bg[0].get_rect()
        self.level = level
        self.reset()

    def reset(self):
        self.x = 0
        self.blocks = pg.sprite.Group()
        self.brick_group = pg.sprite.Group()
        self.coin_boxes = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        self.powerup_group = pg.sprite.Group()
        self.shroom_group = pg.sprite.Group()
        self.finish_flag = None
        self.setup()
        self.top = False
        self.view_point_x = None
        self.view_point_y = None
        self.panned_right = False
        self.panned = False
        self.bg_length = None
        self.bg_height = None

    def start(self):
        if not self.panned_right:
            self.pan_screen()
        elif not self.panned:
            self.pan_left()

    def draw(self):
        # if not self.panned:
        #     self.start()
        # else:

        x = self.mario.vel.x
        self.move_screen(x)
        # self.blit_rect(frame_index)
        self.screen.blit(self.bg[self.level], (self.x, 0))
        # print(self.ground)

    def blit_rect(self):
        # self.blocks.draw(self.screen)
        self.check_mario_collisions()
        self.coin_boxes.update()
        self.coin_boxes.draw(self.screen)
        self.brick_group.draw(self.screen)
        self.platform_group.update()
        for enemy in self.enemies:
            # enemy.update()
            enemy.blitme()
            self.check_enemy_collisions(enemy)
        # self.platform_group.draw(self.screen)
        self.finish_flag.draw()
        for shroom in self.shroom_group:
            if shroom.state != REVEALING:
                self.adjust_mushroom_position(shroom)

        # self.brick_group.draw()

    def move_items(self, vel):
        for coin in self.coin_group.sprites():
            coin.rect.x -= vel
        for powerup in self.powerup_group.sprites():
            powerup.rect.x -= vel
        for shroom in self.shroom_group.sprites():
            shroom.rect.x -= vel
        for coin_box in self.coin_boxes.sprites():
            coin_box.rect.x -= vel
        for block in self.blocks.sprites():
            block.rect.x -= vel
        for brick in self.brick_group.sprites():
            brick.rect.x -= vel
        for enemy in self.enemies:
            enemy.rect.x -= vel
        self.finish_flag.rect.x -= vel

    def move_screen(self, vel):
        if -self.x < self.bg[self.level].get_rect().width - self.screen.get_rect().width:
            self.x -= vel
            self.move_items(vel)
        else:
            self.finish_flag.win()

    def pan_screen(self):
        if -self.x < self.bg_length:
            self.x -= 10
            self.move_items(10)
            # self.mario.rect.x -= 10
        else:
            self.panned_right = True

    def pan_left(self):
        if -self.x > 0:
            self.x -= -10
            self.move_items(-10)
            # self.mario.rect.x -= -10
        else:
            self.panned = True

    def new_level(self):
        if self.level < 7:
            self.x = 0  # set starting position on map
            self.level += 1

    def setup_invisible_rect(self):
        pass

    def setup_boxes(self):
        pass

    def setup_bricks(self):
        pass

    def setup_flag(self):
        pass

    def setup_enemies(self):
        pass

    def setup(self):
        self.setup_boxes()
        self.setup_invisible_rect()
        self.setup_bricks()
        self.setup_flag()
        self.setup_groups()
        self.setup_enemies()

    def setup_groups(self):
        self.platform_group = pg.sprite.Group(self.coin_boxes, self.blocks, self.brick_group)

    def check_y_collisions(self, obj):
        collider = pg.sprite.spritecollideany(obj, self.platform_group)

        if collider:
            self.adjust_y_position(obj, collider)
        else:
            self.check_if_falling(obj, self.platform_group)

    def check_x_collisions(self, obj):
        collider = pg.sprite.spritecollideany(obj, self.platform_group)

        if collider:
            self.adjust_x_position(obj, collider)

    def adjust_mushroom_position(self, mushroom):
        if mushroom.state != REVEALING:
            mushroom.rect.y += mushroom.y_vel
            self.check_y_collisions(mushroom)

            mushroom.rect.x += mushroom.x_vel
            self.check_x_collisions(mushroom)
            self.delete_off_screen(mushroom)

    def check_if_falling(self, obj, group):
        obj.rect.y += 1

        if pg.sprite.spritecollideany(obj, group) is None:
            obj.state = FALLING
        else:
            obj.state = SLIDING

        obj.rect.y -= 1

    def adjust_y_position(self, obj, collider):
        # FALLING
        if obj.rect.bottom + 3 <= collider.rect.bottom:
            obj.state = SLIDING
            if obj.rect.bottom != collider.rect.top:
                obj.rect.bottom = collider.rect.top
                obj.y_vel = 0

    def adjust_x_position(self, obj, collider):
        if obj.rect.x < collider.rect.x:
            obj.rect.right = collider.rect.x
            obj.direction = LEFT
        else:
            obj.rect.x = collider.rect.right
            obj.direction = RIGHT

    def delete_off_screen(self, sprite):
        if sprite.rect.y > self.bg_height:
            sprite.kill()
        elif sprite.rect.y < 0:
            sprite.kill()

    def check_enemy_y_collisions(self, enemy):
        collider = pg.sprite.spritecollideany(enemy, self.platform_group)
        if collider:
            self.adjust_enemy_y_position(enemy, collider)
        else:
            self.check_if_enemy_falling(enemy, self.platform_group)

    def adjust_enemy_y_position(self, enemy, collider):
        if enemy.rect.bottom + 3 <= collider.rect.bottom:
            if enemy.rect.bottom != collider.rect.top:
                enemy.rect.bottom = collider.rect.top

    def check_if_enemy_falling(self, enemy, collider):
        enemy.rect.y += 1

        if pg.sprite.spritecollideany(enemy, collider) is None:
            enemy.fall()

        enemy.rect.y -= 1

    # WONKY
    def check_enemy_x_collisions(self, enemy):
        collider = pg.sprite.spritecollideany(enemy, self.platform_group)
        if collider:
            self.adjust_enemy_x_position(enemy, collider)

    # WONKY
    def adjust_enemy_x_position(self, enemy, collider):
        if enemy.rect.x < collider.rect.x:
            enemy.rect.right = collider.rect.x
            enemy.dir = -enemy.dir
        else:
            enemy.rect.x = collider.rect.right
            enemy.direction = RIGHT

    # UNTESTED
    def check_enemy_collisions(self, enemy):
        self.check_enemy_x_collisions(enemy)

        self.check_enemy_y_collisions(enemy)

    def check_mario_powerup_collisions(self):
        mario_powerup = pg.sprite.spritecollideany(self.mario, self.powerup_group)
        mario_shroom = pg.sprite.spritecollideany(self.mario, self.shroom_group)

        if mario_shroom:
            if mario_shroom.name == MAGICMUSHROOM:
                self.mario.mode = SUPER

        if mario_powerup:
            if mario_powerup.name == FLOWER:
                self.mario.mode = FIRE
            if mario_powerup.name == STAR:
                self.mario.mode = INVINCIBLE

    def win(self):
        pass

    def check_mario_collisions(self):
        self.check_mario_powerup_collisions()
        enemy = pg.sprite.spritecollideany(self.mario, self.enemies)
        collider = pg.sprite.spritecollideany(self.mario, self.blocks)
        coin_box = pg.sprite.spritecollideany(self.mario, self.coin_boxes)
        brick = pg.sprite.spritecollideany(self.mario, self.brick_group)

        if enemy:
            if self.mario.vel.y < 0:
                self.mario.pos.y = enemy.rect.midbottom
                self.mario.vel.y = 0
                self.mario.state = STANDING
                enemy.kill()
                # Death animation
            else:
                self.mario.lives -= 1
                self.mario.reset()
                print(self.mario.lives)

        if collider:
            if self.mario.vel.y > 0:
                self.mario_standing_on_platform(platform=collider)

            elif self.mario.vel.y < 0:
                self.mario.pos.y = collider.rect.bottom + self.mario.rect.height
                self.mario.vel.y = -self.mario.vel.y

        if coin_box:
            if self.mario.vel.y > 0:
                self.mario_standing_on_platform(platform=coin_box)
            elif self.mario.vel.y < 0:
                self.mario.pos.y = coin_box.rect.bottom + self.mario.rect.height
                self.mario.vel.y = -self.mario.vel.y
                coin_box.state = REVEALING

        if brick:
            if self.mario.vel.y > 0:
                self.mario_standing_on_platform(brick)
            elif self.mario.vel.y < 0:
                if self.mario.mode == SUPER or self.mario.mode == FIRE or self.mario.mode == INVINCIBLE:
                    brick.kill()
                else:
                    self.mario.pos.y = brick.rect.bottom + self.mario.rect.height
                    self.mario.vel.y = -self.mario.vel.y

        if pg.sprite.collide_rect(self.mario, self.finish_flag):
            self.win()

    def mario_standing_on_platform(self, platform):
        self.mario.pos.y = platform.rect.top + 1
        self.mario.vel.y = 0
        self.mario.state = STANDING
        self.mario.air_jump = False


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((1200, 600))
    clock = pg.time.Clock()
    # bg = Background(screen=screen, level=0)
    # frame_index = 0
    #
    # while True:
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             pg.quit()
    #             sys.exit()
    #     frame_index += 1
    #     bg.draw()
    #     pg.display.flip()
    #     clock.tick(150)
