import pygame, sys
from pygame import *
from pygame.sprite import *
from spritesheet import SpriteSheet
from settings import *

class Monster(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.sheet = SpriteSheet('images/enemies.png')
        self.images = []
        self.frame = 0
        self.timer = 0
        self.death_timer = 0
        self.animate_timer = 0
        self.duration = 120
        self.dir = -1
        self.gravity = 1.5
        self.state = 'normal'
    
    def prepare(self, x, y, dir, name, add_frames):
        self.name = name
        add_frames()
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.bottom = HEIGHT
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.dir = dir
        self.set_speed()

    def set_speed(self):
        self.x_spd = .15
        self.y_spd = 0


    #takes images from spritesheet for a given enemy
    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sheet.sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))

        image = pygame.transform.scale(image,
                                       (int(rect.width * 2.5),
                                        int(rect.height * 2.5)))
        return image


    #default move function
    def move(self):
        if self.timer - self.animate_timer > self.duration:
            if self.frame == 0:
                self.frame += 1
            elif self.frame == 1:
                self.frame = 0

            self.animate_timer = self.timer
        self.x += self.x_spd * self.dir
        self.rect.x = self.x


    def fall(self):
         if self.y_spd < 10:
            self.y_spd += self.gravity


    #abstract method, handled by the other enemy classes
    def hit(self):
        pass

    
    #enemy's death animation
    def die(self):
        self.rect.y += self.y_spd
        self.rect.x += self.x_spd
        self.y_spd += self.gravity


    def update(self):
        if self.state == 'normal':
            self.move()
        elif self.state == 'fall':
            self.fall()
        elif self.state == 'hit':
            self.hit()
        elif self.state == 'slide':
            self.slide()
        elif self.state == 'attack':
            self.attack()
        elif self.state == 'dead':
            self.die()

        self.timer += 1
        self.image = self.images[self.frame]

    
    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Goomba(Monster):
    def __init__(self, screen, x, y, dir = -1, name = 'goomba'):
        super().__init__(screen)
        self.prepare(x, y, dir, name, self.add_frames)

    def add_frames(self):
        self.images.append(self.get_image(0, 0, 16, 20))
        self.images.append(self.get_image(30, 0, 16, 20))
        self.images.append(self.get_image(60, 0, 16, 8))

    def hit(self):
        frame = 2

        if self.timer - self.death_timer > 500:
            self.kill()


class Koopa(Monster):
    def __init__(self, screen, x, y, dir = -1, name = 'koopa'):
        super().__init__(screen)
        self.prepare(x, y, dir, name, self.add_frames)
        self.duration = 250
    

    def add_frames(self):
        self.images.append(self.get_image(149, 0, 18, 25))
        self.images.append(self.get_image(179, 0, 18, 25))
        self.images.append(self.get_image(208, 0, 18, 25))
        self.images.append(self.get_image(239, 0, 18, 25))
        self.images.append(self.get_image(359, 5, 18, 15))
        self.images.append(self.get_image(329, 4, 17, 16))


    def hit(self):
        self.x_spd = 0
        self.frame = 2
        shell_y = self.rect.bottom
        shell_x = self.rect.x
        self.rect = self.frames[self.frame].get_rect()
        self.rect.x = shell_x
        self.rect.bottom = shell_y
        

    def slide(self):
        self.x_spd = 10 * self.dir


class Paratroopa(Koopa):
    def __init__(self, screen, x, y, dir = -1, name = 'paratroopa'):
        super().__init__(screen)
        self.prepare(x, y, dir, name, self.add_frames)
    
    def add_frames(self):
        self.images.append(self.get_image(149, 0, 18, 25))
        self.images.append(self.get_image(179, 0, 18, 25))
        self.images.append(self.get_image(208, 0, 18, 25))
        self.images.append(self.get_image(239, 0, 18, 25))
        self.images.append(self.get_image(359, 5, 18, 15))
        self.images.append(self.get_image(329, 4, 17, 16))
        

    def move(self):
        pass

    def die(self):
        pass


class Plant(Monster):
    def __init__(self, screen, x, y, dir = -1, name = 'plant'):
        super().__init__(screen)
        self.prepare(x, y, dir, name, self.add_frames)
        self.origin = self.rect.y
        self.uptime = time.get_ticks()
        self.stop_timer = 0
    
    def add_frames(self):
        self.images.append(self.get_image(389, 30, 18, 25))
        self.images.append(self.get_image(419, 30, 17, 24))

    def move(self):
        if self.rect.bottom == self.origin or\
            self.rect.top == self.origin:
            self.y_spd = 0
            self.stop_timer = time.get_ticks()
        else:
            self.uptime = time.get_ticks()
        
        if self.uptime - self.stop_timer == 500:
            self.dir *= -1        

        self.y += self.y_spd * self.dir
        self.rect.y = self.y

    def die(self):
        pass


class Cheep(Monster):
    def __init__(self, screen, x, y, dir = -1, name = 'cheep'):
        super().__init__(screen)
        self.prepare(x, y, dir, name, self.add_frames)
        self.top_pos = 200
    
    def add_frames(self):
        self.images.append(self.get_image(0, 183, 16, 19))
        self.images.append(self.get_image(29, 184, 18, 18))
        self.images.append(self.get_image(59, 183, 18, 18))
        self.images.append(self.get_image(88, 183, 18, 18))

    def move(self):
        if self.rect.y == self.top_pos:
            self.dir *= -1
        self.x += self.x_spd * self.dir
        self.y += self.y_spd * self.dir

    def die(self):
        pass


class Blooper(Monster):
    def __init__(self, screen, x, y, dir, name = 'blooper'):
        super().__init__(screen)
        self.prepare(x, y, dir, name, self.add_frames)
    
    def add_frames(self):
        self.images.append(self.get_image(419, 0, 17, 26))
        self.images.append(self.get_image(389, 4, 18, 28))
    
    def move(self):
        pass

    def hit(self):
        pass

    def die(self):
        pass


class Bowser(Monster):
    def __init__(self, screen, x, y, dir, name = 'bowser'):
        super().__init__(screen)
        self.prepare(x, y, dir, name, self.add_frames)
    
    def add_frames(self):
        self.images.append(self.get_image(1, 210, 34, 34))
        self.images.append(self.get_image(41, 210, 34, 34))
        self.images.append(self.get_image(81, 210, 34, 34))
        self.images.append(self.get_image(121, 210, 34, 34))
        self.images.append(self.get_image(161, 210, 34, 34))
        self.images.append(self.get_image(201, 210, 34, 34))
        self.images.append(self.get_image(241, 210, 34, 34))
        self.images.append(self.get_image(281, 210, 34, 34))

    def move(self):
        pass

    def hit(self):
        pass

    def die(self):
        pass


class Fire_Breath(Monster):
    def __init__(self, screen, x, y, dir, name = 'fire_breath'):
        super().__init__(screen)
        self.prepare(x, y, dir, name, self.add_frames)
        self.x_spd = .3
        self.y_spd = 0
    
    def add_frames(self):
        self.images.append(self.get_image(100, 252, 26, 9))
        self.images.append(self.get_image(131, 252, 26, 9))
        self.images.append(self.get_image(161, 252, 26, 9))
        self.images.append(self.get_image(191, 252, 26, 9))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    enemy = Koopa(screen, 200, 200, -1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #screen.fill((255,255,255))
        screen.fill((0,0,0))
        enemy.update()
        enemy.blitme()
        pygame.display.flip()
    
