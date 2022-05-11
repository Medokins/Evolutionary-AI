import pygame as pg
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.channelTime = 0
        self.isChanneling = False
        self.left_flag = False
        self.right_flag = False

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update(self.isChanneling)
            self.draw()

    def update(self, isChanneling):
        self.all_sprites.update(isChanneling)
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.channelTime = pg.time.get_ticks()
                    self.isChanneling = True
                if event.key == pg.K_a or event.key == pg.K_LEFT and self.isChanneling:
                    self.left_flag = True
                if event.key == pg.K_d or event.key == pg.K_RIGHT and self.isChanneling:
                    self.right_flag = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE and self.left_flag:
                    self.channelTime = pg.time.get_ticks() - self.channelTime
                    jump_height = min(20, self.channelTime // 15)
                    self.player.jumpLeft(jump_height)
                    self.left_flag = False
                    self.right_flag = False
                    self.isChanneling = False
                elif event.key == pg.K_SPACE and self.right_flag:
                    self.channelTime = pg.time.get_ticks() - self.channelTime
                    jump_height = min(20, self.channelTime // 15)
                    self.player.jumpRight(jump_height)
                    self.left_flag = False
                    self.right_flag = False
                    self.isChanneling = False
                elif event.key == pg.K_SPACE:
                    self.channelTime = pg.time.get_ticks() - self.channelTime
                    jump_height = min(20, self.channelTime // 15)
                    self.player.jump(jump_height)
                    self.isChanneling = False
                    self.left_flag = False
                    self.right_flag = False

    def draw(self):
        self.screen.fill((23, 23, 23))
        self.all_sprites.draw(self.screen)
        pg.display.flip()


g = Game()
while g.running:
    g.new()

pg.quit()