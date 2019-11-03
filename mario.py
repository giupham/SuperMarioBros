import pygame as pg
from settings import *
vec = pg.math.Vector2


class Mario(pg.sprite.Sprite):

    def __init__(self, game): # centerx, bottom , screen
        super().__init__()
        self.state = STANDING
        self.direction = RIGHT
        self.mode = NORMAL
        self.walkCount = 0
        self.runCount = 0
        self.slideCount = 0
        self.jumpCount = 0
        self.crouchCount = 0

        self.fireThrowCount = 0
        self.game = game
        self.reset()
        self.setup_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT /2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def setup_frames(self):
        self.frames = []
        for i in range(16):
            frame = pg.image.load('images/{}/{}.png'.format(self.mode, i))
            if self.mode == NORMAL:
                frame = pg.transform.scale(frame, (30, 40)).convert()
            elif self.mode == SUPER:
                frame = pg.transform.scale(frame, (60, 105)).convert()
            elif self.mode == FIRE:
                frame = pg.transform.scale(frame, (60, 105)).convert()
            self.frames.append(frame)

        self.frames_trans1 = []
        for i in range(16):
            frame = pg.image.load('images/{}/{}.png'.format(self.mode, i))
            frame = pg.transform.scale(frame, (30, 40)).convert()
            self.frames_trans1.append(frame)

        self.frames_trans2 = []
        for i in range(16):
            frame = pg.image.load('images/{}/{}.png'.format(self.mode, i))
            frame = pg.transform.scale(frame, (30, 40)).convert()
            self.frames_trans2.append(frame)

        self.left_frames = []
        for x in range(0, 6):
            self.left_frames.append(self.frames[x])
        self.left_frames.append(self.frames[12])
        self.left_frames.append(self.frames[14])

        self.right_frames = []
        for x in range(11, 5, -1):
            self.right_frames.append(self.frames[x])
        self.right_frames.append(self.frames[13])
        self.left_frames.append(self.frames[15])

        self.left_frames_trans1 = []
        for x in range(0, 6):
            self.left_frames_trans1.append(self.frames_trans1[x])

        self.right_frames_trans1 = []
        for x in range(11, 5, -1):
            self.right_frames_trans1.append(self.frames_trans1[x])

        self.left_frames_trans2 = []
        for x in range(0, 6):
            self.left_frames_trans2.append(self.frames_trans2[x])

        self.right_frames_trans2 = []
        for x in range(11, 5, -1):
            self.right_frames_trans2.append(self.frames_trans2[x])

        self.walk_left_frames = []
        self.walk_right_frames = []
        for x in range(2, 5):
            self.walk_left_frames.append(self.left_frames[x])
            self.walk_right_frames.append(self.right_frames[x])

        self.walk_left_frames_trans1 = []
        self.walk_right_frames_trans1 = []
        for x in range(2, 5):
            self.walk_left_frames_trans1.append(self.left_frames_trans1[x])
            self.walk_right_frames_trans1.append(self.right_frames_trans1[x])

        self.walk_left_frames_trans2 = []
        self.walk_right_frames_trans2 = []
        for x in range(2, 5):
            self.walk_left_frames_trans2.append(self.left_frames_trans2[x])
            self.walk_right_frames_trans2.append(self.right_frames_trans2[x])

    def jump(self):
        print(self.jumpCount)
        if self.jumpCount == 0:
            self.rect.y += 1
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            self.rect.y -= 1
            if hits:
                self.vel.y -= 15
                self.jumpCount += 1
        elif self.jumpCount > 0:
            ####
            self.vel.y -= 15
            self.jumpCount += 1
        if not self.state == JUMPING:
            self.jumpCount = 0

    def reset(self):
        self.state = STANDING
        self.direction = RIGHT
        self.mode = FIRE
        self.walkCount = 0
        self.runCount = 0
        self.slideCount = 0
        self.jumpCount = 0
        self.crouchCount = 0

        self.fireThrowCount = 0

    def draw(self, win):
        win.blit(self.image, self.rect)

    def update(self):
        # print(self.state)
        self.acc = vec(0, 0.5)
        keys = pg.key.get_pressed()
        hold_bottom, hold_left = -1, -1

        if self.state == STANDING:
            if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
                self.state = STANDING
            elif keys[pg.K_RIGHT]:
                pg.key.set_repeat(100, 1000)
                self.state = WALKING
                self.direction = RIGHT
            elif keys[pg.K_LEFT]:
                pg.key.set_repeat(100, 1000)
                self.state = WALKING
                self.direction = LEFT
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                pg.key.set_repeat(100, 1000)
                self.state = RUNNING
            elif keys[pg.K_SPACE]:
                self.state = JUMPING
                self.jump()
            elif keys[pg.K_DOWN]:
                self.state = CROUCHING
            elif not any(keys):   #NK
                self.state = STANDING
        if self.state == WALKING:
            if self.direction == RIGHT:
                self.acc.x += PLAYER_ACC
            elif self.direction == LEFT:
                self.acc.x += -PLAYER_ACC
            if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
                self.state = GLIDING
            elif keys[pg.K_RIGHT]:
                pg.key.set_repeat(100, 1000)
                self.state = WALKING
                self.direction = RIGHT
            elif keys[pg.K_LEFT]:
                pg.key.set_repeat(100, 1000)
                self.state = WALKING
                self.direction = LEFT
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                pg.key.set_repeat(100, 1000)
                self.state = RUNNING
            elif keys[pg.K_SPACE]:
                self.state = JUMPING
                self.jump()
            elif keys[pg.K_DOWN]:
                self.state = CROUCHING
            elif not any(keys):   #NK
                self.state = GLIDING
        if self.state == RUNNING:
            if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
                self.state = GLIDING
            elif keys[pg.K_RIGHT]:
                pg.key.set_repeat(100, 1000)
                self.state = WALKING
                self.direction = RIGHT
            elif keys[pg.K_LEFT]:
                pg.key.set_repeat(100, 1000)
                self.state = WALKING
                self.direction = LEFT
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                pg.key.set_repeat(100, 1000)
                self.state = RUNNING
            elif keys[pg.K_SPACE]:
                self.state = JUMPING
                self.jump()
            elif keys[pg.K_DOWN]:
                self.state = CROUCHING
            elif not any(keys):   #NK
                self.state = GLIDING
        if self.state == GLIDING:
            if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
                self.state = WALKING
            elif keys[pg.K_RIGHT]:
                pg.key.set_repeat(100, 1000)
                self.state = WALKING
                self.direction = RIGHT
            elif keys[pg.K_LEFT]:
                pg.key.set_repeat(100, 1000)
                self.state = WALKING
                self.direction = LEFT
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                pg.key.set_repeat(100, 1000)
                self.state = RUNNING
            elif keys[pg.K_SPACE]:
                self.state = JUMPING
                self.jump()
            elif keys[pg.K_DOWN]:
                self.state = CROUCHING
            elif not any(keys):   #NK
                self.state = STANDING
        if self.state == STANDING:
            if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
                self.state = STANDING
            elif keys[pg.K_RIGHT]:
                pg.key.set_repeat(100, 1000)
                self.state = WALKING
                self.direction = RIGHT
            elif keys[pg.K_LEFT]:
                pg.key.set_repeat(100, 1000)
                self.state = WALKING
                self.direction = LEFT
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                pg.key.set_repeat(100, 1000)
                self.state = RUNNING
            elif keys[pg.K_SPACE]:
                self.state = JUMPING
                self.jump()
            elif keys[pg.K_DOWN]:
                self.state = CROUCHING
            elif not any(keys):   #NK
                self.state = STANDING
        if self.state == JUMPING:
            if keys[pg.K_RIGHT]:
                self.direction = RIGHT
                self.acc.x += PLAYER_ACC
            elif keys[pg.K_LEFT]:
                self.direction = LEFT
                self.acc.x += -PLAYER_ACC
            elif keys[pg.K_SPACE]:
                self.state = JUMPING
        if self.state == CROUCHING:
            test = not keys[pg.K_DOWN]
            if not keys[pg.K_DOWN]:
                hold_bottom = self.rect.bottom
                hold_left = self.rect.left

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

        if not hold_left == -1:
            self.update_frame(hold_bottom, hold_left)
            self.state = STANDING
        else:
            self.update_frame()

        # print(self.state, self.walkCount)

    def update_frame(self, bottom = None, left = None):
        if self.direction == LEFT:
            if self.state == STANDING:
                if self.mode == NORMAL or self.mode == SUPER or self.mode == FIRE:
                    self.image = self.left_frames[5]
                elif self.mode == INVINC:
                    self.image = self.left_frames_trans1[5]
                    self.mode == INVINC2
                elif self.mode == INVINC2:
                    self.image = self.left_frames_trans2[5]
                    self.mode == INVINC
                if bottom and left:
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    self.rect.left = left
                self.walkCount = 0
            elif self.state == WALKING:
                walk = self.walkCount//5
                if self.mode == NORMAL or self.mode == SUPER or self.mode == FIRE:
                    self.image = self.walk_left_frames[walk]
                elif self.mode == INVINC:
                    self.image = self.walk_left_frames_trans1[walk]
                    self.mode = INVINC2
                elif self.mode == INVINC2:
                    self.image = self.walk_left_frames_trans2[walk]
                    self.mode = INVINC
            elif self.state == RUNNING:
                walk = self.walkCount//5
                if self.mode == NORMAL or self.mode == SUPER or self.mode == FIRE:
                    self.image = self.walk_left_frames[walk]
                elif self.mode == INVINC:
                    self.image = self.walk_left_frames_trans1[walk]
                    self.mode = INVINC2
                elif self.mode == INVINC2:
                    self.image = self.walk_left_frames_trans2[walk]
                    self.mode = INVINC
            elif self.state == GLIDING:
                if self.mode == NORMAL or self.mode == SUPER or self.mode == FIRE:
                    self.image = self.left_frames[1]
                elif self.mode == INVINC:
                    self.image = self.left_frames_trans1[1]
                    self.mode = INVINC2
                elif self.mode == INVINC2:
                    self.image = self.left_frames_trans2[1]
                    self.mode = INVINC
            elif self.state == JUMPING:
                if self.mode == NORMAL or self.mode == SUPER or self.mode == FIRE:
                    self.image = self.left_frames[0]
                elif self.mode == INVINC:
                    self.image = self.left_frames_trans1[0]
                    self.mode = INVINC2
                elif self.mode == INVINC2:
                    self.image = self.left_frames_trans2[0]
                    self.mode = INVINC
            elif self.state == CROUCHING:
                if self.mode == NORMAL or self.mode == SUPER or self.mode == FIRE:
                    self.image = self.left_frames[6]
                elif self.mode == INVINC:
                    self.image = self.left_frames_trans1[6]
                    self.mode = INVINC2
                elif self.mode == INVINC2:
                    self.image = self.left_frames_trans2[6]
                    self.mode = INVINC
                self.image = pg.transform.scale(self.image, (60, 70)).convert()
                bottom = self.rect.bottom
                left = self.rect.left
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.left = left
        elif self.direction == RIGHT:
            if self.state == STANDING:
                if self.mode == NORMAL or self.mode == SUPER or self.mode == FIRE:
                    self.image = self.right_frames[5]
                elif self.mode == INVINC:
                    self.image = self.right_frames_trans1[5]
                    self.mode = INVINC2
                elif self.mode == INVINC2:
                    self.image = self.right_frames_trans2[5]
                    self.mode = INVINC
                self.walkCount = 0
            elif self.state == WALKING:
                walk = self.walkCount//5
                if self.mode == NORMAL or self.mode == SUPER or self.mode == FIRE:
                    self.image = self.walk_right_frames[walk]
                elif self.mode == INVINC:
                    self.image = self.walk_right_frames_trans1[walk]
                elif self.mode == INVINC2:
                    self.image = self.walk_right_frames_trans2[walk]
                    self.mode = INVINC
        self.walkCount += 1
        if self.walkCount >= 15:
            self.walkCount = 0




