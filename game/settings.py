import pygame
import os

PLAYER_IMGS = pygame.image.load(os.path.join('game', 'Images', 'Character.png'))
GROUND_IMGS = pygame.image.load(os.path.join('game', 'Images', 'Character.png'))
WIDTH, HEIGHT = 1920, 1080 #2560, 1440
FPS = 60
JUMP_HEIGHT_MAX = 3
PLAYER_SIZE = (128,128)
PLAYER_IMG = pygame.transform.scale(PLAYER_IMGS, PLAYER_SIZE)