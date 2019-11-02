import pygame as pg
from settings import *
vec = pg.math.Vector2

class Mario(pg.sprite.Sprite):

    def __init__(self, game): # centerx, bottom , screen
        super().__init__()
        self.game = game
        self.reset()
        self.setup_frames()
        self.image = self.small_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT /2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def setup_frames(self):
        self.small_frames = []
        for i in range(12):
            frame = pg.image.load('images/Mario/{}.png'.format(i))
            frame = pg.transform.scale(frame, (30, 40)).convert()
            self.small_frames.append(frame)

        self.left_frames = []
        for x in range(0, 6):
            self.left_frames.append(self.small_frames[x])

        self.right_frames = []
        for x in range(11, 5, -1):
            self.right_frames.append(self.small_frames[x])

        self.walk_left_frames = []
        self.walk_right_frames = []
        for x in range(2, 5):
            self.walk_left_frames.append(self.left_frames[x])
            self.walk_right_frames.append(self.right_frames[x])

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.state = JUMPING
            self.vel.y -= 20


    def reset(self):
        self.state = STANDING
        self.direction = RIGHT
        self.walkCount = 0
        self.runCount = 0
        self.slideCount = 0
        self.jumpCount = 0
        self.crounchCount = 0

        self.fireThrowCount = 0

    def draw(self, win):
        win.blit(self.image, self.rect)

    def update(self):
        self.update_frame()
        self.acc = vec(0, 0.5)
        keys = pg.key.get_pressed()

        if self.state == STANDING:
            if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
                self.state == STANDING
            if keys[pg.K_RIGHT]:
                self.state == WALKING
            if keys[pg.K_LEFT]:
                self.state == WALKING
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                self.state == RUNNING
            if keys[pg.K_SPACE]:
                self.state == JUMPING
            if keys[pg.K_DOWN]:
                self.state == CROUCHING
            if any(keys):   #NK
                self.state == STANDING

        if self.state == WALKING:
            if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
                self.state == GLIDING
            if keys[pg.K_RIGHT]:
                self.state == WALKING
            if keys[pg.K_LEFT]:
                self.state == WALKING
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                self.state == RUNNING
            if keys[pg.K_SPACE]:
                self.state == JUMPING
            if keys[pg.K_DOWN]:
                self.state == CROUCHING
            if any(keys):   #NK
                self.state == GLIDING

        if self.state == RUNNING:
            if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
                self.state == GLIDING
            if keys[pg.K_RIGHT]:
                self.state == WALKING
            if keys[pg.K_LEFT]:
                self.state == WALKING
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                self.state == RUNNING
            if keys[pg.K_SPACE]:
                self.state == JUMPING
            if keys[pg.K_DOWN]:
                self.state == CROUCHING
            if any(keys):   #NK
                self.state == GLIDING

        if self.state == GLIDING:
            if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
                self.state == WALKING
            if keys[pg.K_RIGHT]:
                self.state == WALKING
            if keys[pg.K_LEFT]:
                self.state == WALKING
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                self.state == RUNNING
            if keys[pg.K_SPACE]:
                self.state == JUMPING
            if keys[pg.K_DOWN]:
                self.state == CROUCHING
            if any(keys):   #NK
                self.state == STANDING

        if self.state == STANDING:
            if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
                self.state == STANDING
            if keys[pg.K_RIGHT]:
                self.state == WALKING
            if keys[pg.K_LEFT]:
                self.state == WALKING
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                self.state == RUNNING
            if keys[pg.K_SPACE]:
                self.state == JUMPING
            if keys[pg.K_DOWN]:
                self.state == CROUCHING
            if any(keys):   #NK
                self.state == STANDING

        # APPLY FRICTION
        # Faster you're going the more friction slows you down
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # APPLY THE ACCELERATION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def update_frame(self):
        if self.direction == LEFT:
            if self.state == STANDING:
                self.image = self.left_frames[5]
            elif self.state == WALKING:
                walk = self.walkCount//5
                self.image = self.walk_left_frames[walk % 3]
                self.walkCount += 1
                if self.walkCount > 15:
                    self.walkCount = 0
        if self.direction == RIGHT:
            if self.state == STANDING:
                self.image = self.right_frames[5]
            elif self.state == WALKING:
                walk = self.walkCount//5
                self.image = self.walk_right_frames[walk % 3]
                self.walkCount += 1
                if self.walkCount > 15:
                    self.walkCount = 0



