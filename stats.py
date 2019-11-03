
class Stats:
    def __init__(self, mario):
        self.reset()
        self.mario = mario

    def reset(self):
        self.coins = 0
        self.points = 0

    def new_life(self):
        if self.coins >= 100:
            self.mario.lives += 1

