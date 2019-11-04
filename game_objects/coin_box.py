import pygame
import sys
from settings import *
from game_objects.coin import Coin
from game_objects.powerup import *

class CoinBox(pygame.sprite.Sprite):
    # sprite_sheet = pygame.image.load('../images/tiles-3.png')
    sprite_sheet = pygame.image.load('images/tiles-3.png')

    def __init__(self, screen, x, y, prize='coin', group=None):
        super().__init__()
        self.screen = screen
        self.setup_frames()

        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect()
        self.rect.x = x * BG_SCALER
        self.rect.y = y * BG_SCALER

        self.frames_index = 0

        # so it moves up
        self.y_vel = 0
        self.rest_height = y * BG_SCALER
        self.gravity = 1.2
        self.state = RESTING
        self.prize = prize
        self.group = group
        self.state = RESTING
        self.frame_count = 0

    def update(self):
        if self.state == RESTING:
            self.resting()
        elif self.state == REVEALING:
            self.start_bump()
        elif self.state == BUMPED:
            self.bumped()
        elif self.state == OPENED:
            self.opened()

        # for prize in self.group.sprites():
        #     prize.update()
        #     prize.draw(self.screen)

        self.frame_count += 1

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def get_image(self, x, y, width, height):
        """Extract image from sprite sheet"""
        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(CoinBox.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))

        image = pygame.transform.scale(image,
                                       (int(rect.width * BG_SCALER),
                                        int(rect.height * BG_SCALER)))
        return image

    def setup_frames(self):
        self.frames = []
        self.frames_index = 0
        # frames list
        for i in range(4):
            self.frames.append(
                self.get_image(385 + (16 * i), 1, 15, 15)
            )

    def resting(self):
        if self.state != EMPTY:
            f = self.frame_count // 12  # slow down
            self.image = self.frames[f % 3]
            if self.frame_count >= 108:
                self.frame_count = 0

    def start_bump(self):
        #goes up
        self.y_vel = -6
        self.state = BUMPED

        if self.prize != EMPTY:
            if self.prize == COIN:
                self.group.add(Coin(screen=self.screen, x=self.rect.centerx, y=self.rect.y))
            elif self.prize == STAR:
                self.group.add(Star(x=self.rect.centerx, y=self.rect.top))
            elif self.prize == ONEUPMUSHROOM:
                self.group.add(OneUpMushroom(x=self.rect.centerx, y=self.rect.top))
            elif self.prize == MAGICMUSHROOM:
                self.group.add(MagicMushroom(x=self.rect.centerx, y=self.rect.top))
            elif self.prize == FLOWER:
                self.group.add(FireFlower(x=self.rect.centerx, y=self.rect.top))
            self.prize = EMPTY

    def bumped(self):
        self.rect.y += self.y_vel
        self.y_vel += self.gravity
        if self.rect.y >= self.rest_height:
            self.frame_index = 3
            self.image = self.frames[self.frame_index]
            self.rect.y = self.rest_height
            self.state = OPENED

    def opened(self):
        self.state = EMPTY
        self.prize = EMPTY

if __name__ == '__main__':
    pygame.init()
    output_screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    prize_group = pygame.sprite.Group()
    coin_box = CoinBox(screen=output_screen, x=600, y=400, prize=COIN, group=prize_group)

    frame_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        output_screen.fill(BLACK)
        frame_index += 1
        coin_box.update()
        coin_box.draw()
        pygame.display.flip()
        clock.tick(FPS)
