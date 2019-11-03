import pygame
import sys
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen

        self.sprite_sheet = pygame.image.load('images/tiles-2.png')
        self.frames = []
        self.frames_index = 0
        self.get_tile_images()

        self.image = self.frames[self.frames_index]

        self.rect = self.image.get_rect()
        self.rect.x = x * BG_SCALER
        self.rect.y = y * BG_SCALER

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""

        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))

        image = pygame.transform.scale(image,
                                       (int(width * BG_SCALER),
                                        int(height * BG_SCALER)))
        return image

    def get_tile_images(self):
        # Bricks
        self.frames.append(
            self.get_image(x=28, y=0, width=17, height=15))


if __name__ == '__main__':
    pygame.init()
    output_screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    tile = Tile(screen=output_screen, x=600, y=400)
    frame_index = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        tile.draw()
        pygame.display.flip()
        clock.tick(150)
