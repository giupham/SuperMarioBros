import pygame as pg
from settings import *

class Collider(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pg.Surface((width * BG_SCALER, height * BG_SCALER)).convert()

        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x * BG_SCALER
        self.rect.y = y * BG_SCALER

    def __str__(self):
        return str(self.rect.x) + "," + str(self.rect.y)


