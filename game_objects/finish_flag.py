import pygame
from settings import *

class Flag(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, box_height):
        super().__init__()
        # Enter image here
        self.image = pygame.image.load('images/4.png')
        self.rect = self.image.get_rect()
        self.rect.x = x * BG_SCALER
        self.rect.y = y * BG_SCALER
        self.image = pygame.transform.scale(self.image,
                                            (int(self.rect.width * BG_SCALER),
                                             int(self.rect.height * BG_SCALER)))

        self.box_height = box_height * BG_SCALER
        print(box_height)

        self.screen = screen
        self.bottom = False
        self.vel = 2

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def get_image(self, x, y, width, height):
        """Extract image from sprite sheet"""
        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.image, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))

        image = pygame.transform.scale(self.image,
                                       (int(rect.width * BG_SCALER),
                                        int(rect.height * BG_SCALER)))
        return image

    def win(self):
        if self.rect.bottom > self.box_height:
            self.bottom = True
        if not self.bottom:
            self.rect.y += self.vel


    def update(self):
        pass

if __name__ == '__main__':
    pygame.init()
    output_screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    prize_group = pygame.sprite.Group()
    coin_box = Flag(screen=output_screen, x=30, y=30)
    frame_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        frame_index += 1
        output_screen.fill(BLACK)
        coin_box.update()
        pygame.display.flip()
        clock.tick(FPS)