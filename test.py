for x in range(5, -1, -1):
    print(x)

for frame in self.frames:
    frame.set_colorkey((0, 0, 0))

    def shoot_fireballs(self):
        now = pg.time.get_ticks()
        if now - self.last > 300 and len(self.game.fireballs) <= FIREBALLS_ALLOWED:
            fireball = FireBall(self, self.game)
            self.game.all_sprites.add(fireball)
            self.game.fireballs.add(fireball)
            self.last = now

        self.lives = 3

