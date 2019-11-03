# shrooms, star, invicibility
import pygame
from settings import *

__all__ = ['PowerUp',
           'MagicMushroom',
           'OneUpMushroom',
           'Star',
           'FireFlower']

class PowerUp(pygame.sprite.Sprite):
    # sprite_sheet = pygame.image.load('../images/item_objects.png')
    sprite_sheet = pygame.image.load('images/item_objects.png')

    def __init__(self):
        super().__init__()

    def setup(self, x, y, name, score, setup_frames):
        self.frames = []
        setup_frames()
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.state = REVEALING
        # moves the powerup
        self.y_vel = -2
        self.x_vel = 0
        # original height
        self.box_height = self.rect.y
        self.gravity = 1
        self.max_y_vel = 6
        self.direction = 'right'
        self.name = name
        self.score = score
        self.direction = RIGHT
        self.down = False

    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""

        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(PowerUp.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))

        image = pygame.transform.scale(image,
                                   (int(rect.width * BG_SCALER),
                                    int(rect.height * BG_SCALER)))
        return image

    def revealing(self):
        self.rect.y += self.y_vel
        if self.rect.bottom < self.box_height:
            self.y_vel += self.gravity
        elif self.rect.y > self.box_height:
            self.y_vel = 0
            self.state = SLIDING

    def sliding(self):
        # self.rect.x += self.x_vel
        if self.direction == RIGHT:
            self.x_vel = 3
        else:
            self.x_vel = -3

    def falling(self):
        # self.rect.y += self.y_vel
        if self.y_vel < self.max_y_vel:
            self.y_vel += self.gravity

    def update(self):
        if self.state == REVEALING:
            self.revealing()
        elif self.state == SLIDING:
            self.sliding()
        elif self.state == FALLING:
            self.falling()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class MagicMushroom(PowerUp):
    def __init__(self, x, y):
        super().__init__()
        self.setup(x=x, y=y, name=MAGICMUSHROOM, score=100, setup_frames=self.setup_frames)

    def setup_frames(self):
        self.frames.append(
            self.get_image(x=143, y=16, width=17, height=16))

class OneUpMushroom(PowerUp):
    def __init__(self, x, y):
        super().__init__()
        self.setup(x=x, y=y, name=ONEUPMUSHROOM, score=20, setup_frames=self.setup_frames)

    def setup_frames(self):
        self.frames.append(
            self.get_image(x=143, y=0, width=17, height=16))

class Star(PowerUp):
    def __init__(self, x, y):
        super().__init__()
        self.setup(x=x, y=y, name=STAR, score=100, setup_frames=self.setup_frames)

    def setup_frames(self):
        self.frames.append(
            self.get_image(x=143, y=48, width=18, height=16))

    def update(self):
        self.revealing()

class FireFlower(PowerUp):
    def __init__(self, x, y):
        super().__init__()
        self.setup(x=x, y=y, name=FLOWER, score=100, setup_frames=self.setup_frames)

    def setup_frames(self):
        self.frames.append(
            self.get_image(x=144, y=31, width=16, height=17))

    def update(self):
        self.revealing()


if __name__ == '__main__':
    pygame.init()
    output_screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    # group = pygame.sprite.Group(MagicMushroom(x=200, y=200),
    #                             OneUpMushroom(x=200, y=300),
    #                             Star(x=300, y=300),
    #                             FireFlower(x=300, y=400))
    shroom = Star(x=100, y=100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        output_screen.blit(shroom.image, shroom.rect)
        shroom.update()

        pygame.display.flip()
        clock.tick(60)
