TITLE = "Jump King"
WIDTH = 1000
HEIGHT = 1000
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Game properties
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1

# platforms, indexes below:
# 2 -> ground, 1 -> short one, 0 (default) -> long one
PLATFORM_LIST = [(0, HEIGHT - 100, 2), # ground

                (112, HEIGHT - 300),
                (WIDTH - 224, HEIGHT - 500),

                (WIDTH / 2 - 112, 80),
                (60, -300),
                (WIDTH - 224, -700),
                (500, -1100),
                (WIDTH - 224, -1500),
                (0, -1900),
                (WIDTH - 224, -2300),

                (WIDTH / 2 - 112, -2700, 1),
                (60, -3000, 1),
                (WIDTH - 224, -3400, 1),
                (500, -3550),
                (WIDTH - 224, -3900, 1),
                (0, -4300, 1),
                (WIDTH - 224, -4600)
                ]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)