# Sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.isJumping = False

    def jump(self, jump_height):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -jump_height
            print("Up")
            self.isJumping = True
    
    def jumpRight(self, jump_height):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -jump_height
            self.vel.x = 10
            self.isJumping = True
            print("Right")

    def jumpLeft(self, jump_height):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -jump_height
            self.vel.x = -10
            self.isJumping = True
            print("Left")


    def update(self, isChanneling):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if not isChanneling and not self.isJumping:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.acc.x = -PLAYER_ACC
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        if pg.sprite.spritecollide(self, self.game.platforms, False):
            self.isJumping = False

        if self.isJumping: #update y but don't update x
            self.vel.y += self.acc.y
        else:
            self.vel += self.acc

        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > WIDTH - 20: self.pos.x = WIDTH - 20
        if self.pos.x - 20 < 0: self.pos.x = 20

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y