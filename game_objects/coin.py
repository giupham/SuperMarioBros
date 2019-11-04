import pygame
from settings import *

class Coin(pygame.sprite.Sprite):
    sprite_sheet = pygame.image.load('images/item_objects.png')
    # sprite_sheet = pygame.image.load('../images/item_objects.png')

    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen

        self.setup_frames()

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.state = REVEALING
        self.name = COIN

        self.box_height = self.rect.y
        # so it moves up
        self.y_vel = -2
        self.gravity = 1
        self.score = 100

    def draw(self, index):
        self.update()
        self.screen.blit(self.image, self.rect)

    def get_image(self, x, y, width, height):
        """Extract image from sprite sheet"""
        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(Coin.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))

        image = pygame.transform.scale(image,
                                       (int(rect.width * BG_SCALER),
                                        int(rect.height * BG_SCALER)))
        return image

    def setup_frames(self):
        self.frames = []
        self.frames_index = 0
        # frames list
        # for i in range(4):
        #     self.frames.append(
        #         self.get_image(16*i, 97, 16, 16))
        # for i in range(4):
        #     self.frames.append(
        #         self.get_image(16*i, 113, 16, 16))
        self.frames.append(self.get_image(0, 97, 16, 16))

    def revealing(self):
        self.rect.y += self.y_vel
        if self.rect.bottom < self.box_height - 5:
            self.y_vel += self.gravity
        elif self.rect.y >= self.box_height:
            self.y_vel = 0
            self.state = RESTING
            self.kill()

    def update(self):
        if self.state == REVEALING:
            self.revealing()



if __name__ == '__main__':
    pygame.init()
    output_screen = pygame.display.set_mode((1200, 800))
    output_screen.fill(GREEN)
    clock = pygame.time.Clock()
    prize_group = pygame.sprite.Group()
    coin_box = Coin(screen=output_screen, x=600, y=400)
    frame_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        frame_index += 1

        coin_box.draw(frame_index)
        pygame.display.flip()
        clock.tick(FPS)