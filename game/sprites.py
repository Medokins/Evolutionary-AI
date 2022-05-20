import pygame as pg
from settings import *
from random import choice
vec = pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width / 2, height / 2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jump_height = 10

    def load_images(self):
        self.standing_frames = [self.game.character_standing[0].get_image(0, 0, 128, 128),
                                self.game.character_standing[1].get_image(0, 0, 128, 128),
                                self.game.character_standing[2].get_image(0, 0, 128, 128)]

        for frame in self.standing_frames:
            frame.set_colorkey(WHITE)

        self.walk_frames_r = [self.game.character_standing[1].get_image(0, 0, 128, 128),
                            self.game.character_standing[1].get_image(0, 0, 128, 128)]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(WHITE)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
    
        self.jump_frame = self.game.character_standing[2].get_image(0, 0, 128, 128)
        self.jump_frame.set_colorkey(WHITE)

    def jump(self):
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits:
            self.vel.y = -self.jump_height
    
    def jumpRight(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -self.jump_height
            self.vel.x = 7

    def jumpLeft(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -self.jump_height
            self.vel.x = -7

    def update(self, isChanneling):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if not isChanneling and not self.jumping:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.acc.x = -PLAYER_ACC
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # if jumping than update y only
        if self.jumping:
            self.vel.y += self.acc.y
        else: 
            self.vel += self.acc

        if abs(self.vel.x) < 0.1: self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > WIDTH - 20: self.pos.x = WIDTH - 20
        if self.pos.x - 20 < 0: self.pos.x = 20

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0: self.walking = True
        else: self.walking = False

        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet[0].get_image(0, 0, 224, 40),
                  self.game.spritesheet[1].get_image(0, 0, 112, 20)]
        self.image = choice(images)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y