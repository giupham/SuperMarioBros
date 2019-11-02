import pygame as pg
import random
from settings import *
from player import *
from mario import Mario

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Mario(game=self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            fall_hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if fall_hits:
                self.player.pos.y = fall_hits[0].rect.top + 1
                self.player.vel.y = 0

        # check if player hits a platform - only if jump
        elif self.player.vel.y < 0:
            jump_hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if jump_hits:
                # print(jump_hits[0].rect.bottom, self.player.pos.y + self.player.rect.height/2)
                self.player.pos.y = jump_hits[0].rect.bottom + self.player.rect.height
                self.player.vel.y = -self.player.vel.y

        # if self.player.vel.x > 0:
        #     right_hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        #     if right_hits:
        #         self.player.pos.x = right_hits[0].rect.left - self.player.rect.width/2
        #         self.player.vel.x = 0
        #
        # elif self.player.vel.x < 0:
        #     left_hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        #     if left_hits:
        #         self.player.pos.x = left_hits[0].rect.right + self.player.rect.width/2
        #         self.player.vel.x = 0


    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()