import pygame, sys
from settings import *
from level import Level
from player import Player, PLAYER_IMG

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
level = Level(level_map, WIN)

def draw_window(x, y):
    WIN.fill((26,26,26))
    WIN.blit(PLAYER_IMG, (x, y))
    level.run()
    pygame.display.update()

def main():
    jumpKing = Player(960, 540)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
        clock.tick(FPS)

if __name__ == "__main__":
    main()