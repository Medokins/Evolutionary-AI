import pygame as pg
from settings import *
vec = pg.math.Vector2


class Spritesheet:
    '''
        utility class for loading and parsing spritesheets
    '''
    def __init__(self, filename):
        '''
            loads images
        '''
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        '''
            creates surface with spritesheet image on it
        '''
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width, height))
        return image

class Player(pg.sprite.Sprite):
    '''
        class for running player movement/animation methods
    '''
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
        self.pos = vec(WIDTH / 2, HEIGHT - 40)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jump_height = 10
        self.channelTime = 0
        self.isChanneling = False
        self.left_flag = False
        self.right_flag = False

    def load_images(self):
        '''
            loads all Player images
        '''
        self.standing_frames = [self.game.character_standing[0].get_image(0, 0, 98, 110),
                                self.game.character_standing[1].get_image(0, 0, 98, 110),
                                self.game.character_standing[2].get_image(0, 0, 94, 110)]

        for frame in self.standing_frames:
            frame.set_colorkey(WHITE)

        self.walk_frames_r = [self.game.character_standing[0].get_image(0, 0, 98, 110),
                              self.game.character_standing[1].get_image(0, 0, 98, 110)]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(WHITE)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
    
        self.jump_frame = self.game.character_standing[2].get_image(0, 0, 128, 128)
        self.jump_frame.set_colorkey(WHITE)

    def jump(self, jump_height):
        '''
            make player jump up
        '''
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits:
            jump_height = min(35, jump_height)
            self.vel.y = -jump_height
    
    def jumpRight(self, jump_height):
        '''
            make player jump right
        '''
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits:
            jump_height = min(35, jump_height)
            self.vel.y = -jump_height
            self.vel.x = 10

    def jumpLeft(self, jump_height):
        '''
            make player jump left
        '''
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits:
            jump_height = min(35, jump_height)
            self.vel.y = -jump_height
            self.vel.x = -10

    def update(self):
        '''
            method that calls animate method, checks for player input (left/right movement)
            and apply movement equation
        '''
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if not self.isChanneling and not self.jumping:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.pos.x += -8
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.pos.x += 8
        if keys[pg.K_n]: self.pos.y -= 100
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # if jumping than update y only
        if self.jumping:
            self.vel.y += self.acc.y
            if abs(self.vel.y) > 40:
                if self.vel.y > 0: self.vel.y = 40
                else: self.vel.y = -40
        else: 
            self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc

        if self.jumping:
            if self.pos.x > WIDTH - 64 or self.pos.x - 64 < 0:
                self.vel.x = -self.vel.x
        else:
            if self.pos.x > WIDTH - 64:
                self.pos.x = WIDTH - 64
            if self.pos.x - 64 < 0:
                self.pos.x = 64

        self.rect.midbottom = self.pos

    def animate(self):
        '''
            animate player movement while walking, jumping and idling
        '''
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
    '''
        class for creating and loading platforms

    '''
    def __init__(self, game, x, y, image_index = 0):
        '''
            crates platform with image with given image_index at x, y coordinate
        '''
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet[0].get_image(0, 0, 224, 40),
                  self.game.spritesheet[1].get_image(0, 0, 112, 20),
                  self.game.spritesheet[2].get_image(0, 0, 1100, 40)]
                  
        self.image = images[image_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y