# game options/settings
TITLE = "Super Mario Bros."
WIDTH = 1200
HEIGHT = 600
FPS = 60

# Player properties
PLAYER_ACC = 0.5
RUNNING_ACC = 0.8
PLAYER_FRICTION = -0.12

# FireBall Speed
FIREBALL_SPEED = 3

FIREBALLS_ALLOWED = 5

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 # (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 30),
                 (125, HEIGHT - 250, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# MARIO STATES
STANDING = 'standing'
WALKING = 'walking'
RUNNING = 'running'
JUMPING = 'jumping'
GLIDING = 'gliding'
CROUCHING = 'crouching'

# Mario Modes
NORMAL = 'Mario'
SUPER = 'SuperMario'
FIRE = 'FireMario'
INVINC = 'StarMario1'
INVINC2 = 'StarMario2'

# MARIO DIRECTIONS
LEFT = 'left'
RIGHT = 'right'
UP = 'up'

BG_SCALER = 2.5

GROUND_HEIGHT = 199

# Coin box status
RESTING = 'resting'
BUMPED = 'bumped'
OPENED = 'opened'
EMPTY = 'empty'

# Coin Box prizes
STAR = 'star'
FLOWER = 'flower'
MAGICMUSHROOM = 'magic mushroom'
ONEUPMUSHROOM = 'one up mushroom'
COIN = 'coin'


# Power up status
REVEALING = 'revealing'
SLIDING = 'sliding'
FALLING = 'falling'



