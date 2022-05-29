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
# 2 -> ground, 1 -> short one, 0  -> long one
PLATFORM_LIST = [
    [(0, HEIGHT - 40, 2), (112, HEIGHT - 300, 0), ((WIDTH - 224)/2, HEIGHT - 800, 2)], #level 1
    [(0, -520, 0)],  #level 2
    [(448, -1050, 2), (-200, -1350, 2), (224, -1600, 0)],#level 3
    [(WIDTH - 448, -2050, 2), (224, -2450, 0)], #level 4
    [(WIDTH - 400, -3050, 0)] #final leap
                ]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)