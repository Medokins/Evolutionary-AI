from turtle import left
import pygame
import os
import time

from torch import chain_matmul
from transformers import PYTORCH_PRETRAINED_BERT_CACHE

PLAYER_IMGS = pygame.image.load(os.path.join('Images', 'Character.png'))
GROUND_IMGS = pygame.image.load(os.path.join('Images', 'Character.png'))
WIDTH, HEIGHT = 1920, 1080 #2560, 1440
FPS = 60
PLAYER_SIZE = (512,512)
PLAYER_IMG = pygame.transform.scale(PLAYER_IMGS, PLAYER_SIZE)

pygame.display.set_caption("Jump King")
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_window(x, y):
    WIN.fill((255,255,255))
    WIN.blit(PLAYER_IMG, (x, y))
    pygame.display.update()

def main():
    channel_time = 0
    run = True
    clock = pygame.time.Clock()
    jumpKing = Player(960, 540)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and channel_time == 0:
                    channel_time = time.time()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    channel_time = 3*(time.time() - channel_time)
                    if channel_time > 3: channel_time = 3
                    jump_height = channel_time
                    jumpKing.isJumping = True
                    channel_time = 0

        userInput = pygame.key.get_pressed()

        if userInput[pygame.K_LEFT] or userInput[pygame.K_a] and jumpKing.x > 0:
            jumpKing.moveLeft()
        if userInput[pygame.K_RIGHT] or userInput[pygame.K_d] and jumpKing.x < WIDTH - PLAYER_SIZE[0]:
            jumpKing.moveRight()
        if jumpKing.isJumping:
            jumpKing.jump(jump_height)

        draw_window(jumpKing.x, jumpKing.y)   

    pygame.quit()

class Player:
    IMGS = PLAYER_IMGS

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 20
        self.vel_x = 10
        self.isJumping = False


    def jump(self, jump_height):      
        '''
        makes player jump when spacebar is pressed
        '''
        self.y -= self.vel_y * jump_height
        if jump_height > 1:
            self.vel_y -= 1
        else:
            self.vel_y -= 2
        if self.vel_y < -20:
            self.vel_y = 20
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

if __name__ == "__main__":
    main()