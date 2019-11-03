import pygame
from background import Background
from settings import *
from game_objects.Collider import Collider
from game_objects.tile import Tile
from game_objects.coin_box import CoinBox
from game_objects.finish_flag import Flag
# from monster import Goomba

import sys


class Level1(Background):
    def __init__(self, screen):
        super().__init__(screen=screen, level=0)
        self.background = self.bg[0]
        self.background_rect = self.bg[0].get_rect()
        self.view_point_x = -self.background_rect.width * BG_SCALER
        self.view_point_y = self.background_rect.height * BG_SCALER
        self.bg_length = self.bg[self.level].get_rect().width - self.screen.get_rect().width
        self.bg_height = self.bg[self.level].get_rect().height

    def setup_invisible_rect(self):
        # Ground
        self.blocks.add(Collider(x=0, y=GROUND_HEIGHT, width=1097, height=26))
        self.blocks.add(Collider(x=1127, y=GROUND_HEIGHT, width=241, height=26))
        self.blocks.add(Collider(x=1418, y=GROUND_HEIGHT, width=1020, height=26))
        self.blocks.add(Collider(x=2473, y=GROUND_HEIGHT, width=911, height=26))

        # Green Tower
        self.blocks.add(Collider(x=440, y=167, width=33, height=34))
        self.blocks.add(Collider(x=600, y=152, width=34, height=47))
        self.blocks.add(Collider(x=730, y=132, width=33, height=68))
        # 1
        self.blocks.add(Collider(x=905, y=135, width=35, height=65))
        # 2
        self.blocks.add(Collider(x=2603, y=167, width=33, height=34))
        self.blocks.add(Collider(x=2859, y=167, width=33, height=34))

        # STAIR BLOCKS
        for i in range(4):
            self.blocks.add(Collider(x=(2140 + (16 * i)),
                                     y=(185 - (16 * i)),
                                     width=(65 - (16 * i)),
                                     height=18))

        # 2nd stair block
        for i in range(4):
            self.blocks.add(Collider(x=2233,
                                     y=(184 - (16 * i)),
                                     width=(65 - (16 * i)),
                                     height=18))

        # 3rd stair block
        for i in range(4):
            self.blocks.add(Collider(x=(2364 + (16 * i)),
                                     y=(184 - (16 * i)),
                                     width=(81 - (16 * i)),
                                     height=18))

        # 4th stair block
        for i in range(4):
            self.blocks.add(Collider(x=2473,
                                     y=(183 - (16 * i)),
                                     width=(65 - (16 * i)),
                                     height=18))

        # 5th stair block
        for i in range(8):
            self.blocks.add(Collider(x=(2897 + (16 * i)),
                                     y=(182 - (16 * i)),
                                     width=(140 - (16 * i)),
                                     height=18))

    def setup_boxes(self):
        self.coin_boxes.add(CoinBox(screen=self.screen, x=250,
                                    y=135, group=self.coin_group))
        self.coin_boxes.add(CoinBox(screen=self.screen, x=329,
                                    y=135, group=self.coin_group))
        self.coin_boxes.add(CoinBox(screen=self.screen, x=346,
                                    y=71, prize=ONEUPMUSHROOM, group=self.shroom_group))
        self.coin_boxes.add(CoinBox(screen=self.screen, x=362,
                                    y=135, group=self.powerup_group))
        self.coin_boxes.add(CoinBox(screen=self.screen, x=1242,
                                    y=136, prize=FLOWER, group=self.powerup_group))
        self.coin_boxes.add(CoinBox(screen=self.screen, x=1690,
                                    y=135, group=self.coin_group))
        self.coin_boxes.add(CoinBox(screen=self.screen, x=1737,
                                    y=135, group=self.coin_group))
        self.coin_boxes.add(CoinBox(screen=self.screen, x=1785,
                                    y=135, group=self.coin_group))
        self.coin_boxes.add(CoinBox(screen=self.screen, x=1737,
                                    y=72, group=self.coin_group))
        self.coin_boxes.add(CoinBox(screen=self.screen, x=2058,
                                    y=72, group=self.coin_group))
        self.coin_boxes.add(CoinBox(screen=self.screen, x=2074,
                                    y=72, group=self.coin_group))
        self.coin_boxes.add(CoinBox(screen=self.screen, x=2715,
                                    y=135, group=self.coin_group))

    def setup_bricks(self):
        self.brick_group.add(Tile(screen=self.screen, x=313, y=136))
        self.brick_group.add(Tile(screen=self.screen, x=344, y=136))
        self.brick_group.add(Tile(screen=self.screen, x=376, y=136))
        self.brick_group.add(Tile(screen=self.screen, x=1225, y=136))
        self.brick_group.add(Tile(screen=self.screen, x=1256, y=136))

        for i in range(7):
            self.brick_group.add(Tile(screen=self.screen, x=1273 + (17 * i), y=72))

        for i in range(3):
            self.brick_group.add(Tile(screen=self.screen, x=1447 + (17 * i), y=72))

        self.brick_group.add(Tile(screen=self.screen, x=1496, y=136))

        for i in range(2):
            self.brick_group.add(Tile(screen=self.screen, x=1593 + (17 * i), y=136))

        self.brick_group.add(Tile(screen=self.screen, x=1881, y=136))

        for i in range(3):
            self.brick_group.add(Tile(screen=self.screen, x=1929 + (17 * i), y=72))

        self.brick_group.add(Tile(screen=self.screen, x=2041, y=72))
        self.brick_group.add(Tile(screen=self.screen, x=2088, y=72))
        for i in range(2):
            self.brick_group.add(Tile(screen=self.screen, x=2057 + (17 * i), y=136))
            self.brick_group.add(Tile(screen=self.screen, x=2680 + (17 * i), y=136))

        self.brick_group.add(Tile(screen=self.screen, x=2728, y=136))

    def setup_flag(self):
        self.finish_flag = Flag(screen=self.screen, x=3152, y=40, box_height=170)

    def setup_enemies(self):
        print('Created')
        self.enemies.add(Goomba(screen=self.screen, x=512, y=GROUND_HEIGHT))
        self.enemies.add(Goomba(screen=self.screen, x=659, y=GROUND_HEIGHT))
        self.enemies.add(Goomba(screen=self.screen, x=1174, y=GROUND_HEIGHT))
        self.enemies.add(Goomba(screen=self.screen, x=1691, y=GROUND_HEIGHT))

    # def check_collide(self, mario, collider):
    #     is_collided = pygame.sprite.spritecollideany(mario, collider)
    #     if is_collided:
    #         if mario.rect.x < is_collided.rect.x:
    #             mario.rect.right = is_collided.rect.left
    #         else:
    #             mario.rect.left = is_collided.rect.left


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    bg = Level1(screen=screen)
    frame_index = 140

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        bg.draw()
        # bg.win()

        bg.blit_rect()
        pygame.display.flip()
        clock.tick(FPS)
