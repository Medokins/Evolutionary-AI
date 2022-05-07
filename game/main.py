import pygame
from settings import *

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not jumpKing.isJumping:
                    channel_time = pygame.time.get_ticks()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and not jumpKing.isJumping:
                    channel_time = pygame.time.get_ticks() - channel_time
                    jump_height = min(JUMP_HEIGHT_MAX, channel_time // 40)
                    jumpKing.isJumping = True

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

if __name__ == "__main__":
    main()