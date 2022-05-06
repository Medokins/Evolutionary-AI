import pygame
import os
import time

PLAYER_IMGS = pygame.image.load(os.path.join('Images', 'Character.png'))
GROUND_IMGS = pygame.image.load(os.path.join('Images', 'temp.png'))
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
    run = True
    clock = pygame.time.Clock()
    jumpKing = Player(960, 540)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        userInput = pygame.key.get_pressed()

        if userInput[pygame.K_LEFT] or userInput[pygame.K_a] and jumpKing.x > 0:
            jumpKing.moveLeft()
        if userInput[pygame.K_RIGHT] or userInput[pygame.K_d] and jumpKing.x < WIDTH - PLAYER_SIZE[0]:
            jumpKing.moveRight()

        if not jumpKing.isJumping and userInput[pygame.K_SPACE]:
            jumpKing.isJumping = True
        if jumpKing.isJumping:
            jumpKing.jump()

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

    def jump(self):      
        '''
        makes player jump when spacebar is pressed
        '''
        self.y -= self.vel_y * 2
        self.vel_y -= 1
        if self.vel_y < -20:
            self.vel_y = 20
            self.isJumping = False
    
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