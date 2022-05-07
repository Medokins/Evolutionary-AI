import pygame
import os
from settings import PLAYER_SIZE

PLAYER_IMGS = pygame.image.load(os.path.join('game', 'Images', 'Character.png'))
GROUND_IMGS = pygame.image.load(os.path.join('game', 'Images', 'Character.png'))
PLAYER_IMG = pygame.transform.scale(PLAYER_IMGS, PLAYER_SIZE)

class Player:
    IMGS = PLAYER_IMGS

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 10
        self.vel_x = 10
        self.isJumping = False


    def jump(self, jump_height):      
        '''
        makes player jump when spacebar is pressed, height of jump is controlled by the time space bar is being pressed
        ''' 
        self.y -= self.vel_y * jump_height
        self.vel_y -= 0.5
        if self.vel_y < -10:
            self.vel_y = 10
            self.isJumping = False
            jump_height = 0

    
    def moveRight(self):
        '''
        makes player move right when right arrow or "d" key is pressed
        '''     
        self.x += self.vel_x

    def moveLeft(self):
        '''
        makes player move left when left arrow or "a" key is pressed
        '''       
        self.x -= self.vel_x
