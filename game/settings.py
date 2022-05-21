TITLE = "Jump King"
WIDTH = 1000
HEIGHT = 1080
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

# platforms
PLATFORM_LIST = [(0, HEIGHT - 100), (224, HEIGHT - 100), (448, HEIGHT - 100),(672, HEIGHT - 100),

                (WIDTH / 2 - 112, HEIGHT - 300),
                (WIDTH - 224, HEIGHT - 500),

                (WIDTH / 2 - 112, 80),
                (0, -300),
                (WIDTH - 224, -700),
                (0, -1100),
                (WIDTH - 224, -1500),
                (0, -1900),
                (WIDTH - 224, -2300)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)