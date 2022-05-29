import pygame as pg 
from settings import *
from sprites import *
from os import path
import numpy as np

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        self.score = 0
        self.player = []
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()


    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        highscore_path = path.join(self.dir, '../game')
        with open(path.join(highscore_path, HS_FILE), 'r') as f:
            try: self.highscore = int(f.read())
            except: self.highscore = 0

        # load images
        img_dir = path.join(self.dir, '../game/Images')            

        # load platform images
        self.spritesheet = [Spritesheet(path.join(img_dir, "platforms", "platform_1.png")),
                            Spritesheet(path.join(img_dir, "platforms", "platform_2.png")),
                            Spritesheet(path.join(img_dir, "platforms", "ground.png"))]

        # load character images
        self.character_standing = [Spritesheet(path.join(img_dir, "standing", "standing1.png")),\
                                   Spritesheet(path.join(img_dir, "standing", "standing2.png")),\
                                   Spritesheet(path.join(img_dir, "standing", "standing3.png"))]

        # load sounds
        self.sound_dir = path.join(self.dir, 'sound')
        

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        highest_player = self.player[0]
        highest = self.player[0].pos.y
        for player in self.player:
            if player.pos.y <= highest:
                highest_player = player

                #if at top of screen
                if highest_player.rect.top < 0:
                    player.level += 1
                    player.pos.y += HEIGHT
                    for plat in self.platforms:
                        plat.rect.y += HEIGHT

                #if player reaches bottom of screen
                if highest_player.rect.top > HEIGHT:
                    player.level -= 1
                    player.pos.y -= HEIGHT
                    for plat in self.platforms:
                        plat.rect.y -= HEIGHT
            
            hits = pg.sprite.spritecollide(player, self.platforms, False)
            if hits:
                # top platform colision (when falling)
                if player.vel.y > 0:
                    if player.pos.x -5 > hits[0].rect.topleft[0] and player.pos.x + 5 < hits[0].rect.topright[0]:
                        if player.pos.y > hits[0].rect.top and player.pos.y < hits[0].rect.bottom:
                            player.vel.x = 0
                            player.pos.y = hits[0].rect.top
                            player.vel.y = 0
                            player.jumping = False

                # bottom platform colision
                elif player.vel.y < 0:
                    if player.pos.x >= hits[0].rect.bottomleft[0] and player.pos.x <= hits[0].rect.bottomright[0]:
                        if player.pos.y - player.rect[1] <= hits[0].rect.top:
                            player.vel.y = 0

                # bouncing off sides
                if (player.pos.x + 30 < hits[0].rect.bottomleft[0] and player.vel.x > 0) or (player.pos.x - 30 > hits[0].rect.bottomright[0] and player.vel.x < 0):
                    if player.jumping:
                        player.vel.x = -player.vel.x

            player.score = int(HEIGHT - player.pos.y + HEIGHT*player.level)
            self.score = highest_player.score
            print(self.find_closest(highest_player))
                    
    def events(self):
        # Game Loop - events
        for player in self.player:
            hits = pg.sprite.spritecollide(player, self.platforms, False)
            if hits:
                player.jumping = False
            else:
                player.jumping = True

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        player.channelTime = pg.time.get_ticks()
                        player.isChanneling = True
                    if event.key == pg.K_a or event.key == pg.K_LEFT and player.isChanneling:
                        player.left_flag = True
                    if event.key == pg.K_d or event.key == pg.K_RIGHT and player.isChanneling:
                        player.right_flag = True

                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE and player.left_flag:
                        player.channelTime = pg.time.get_ticks() - player.channelTime
                        player.jumpLeft(min(35, player.channelTime // 10))
                        player.left_flag = False
                        player.right_flag = False
                        player.isChanneling = False
                    elif event.key == pg.K_SPACE and player.right_flag:
                        player.channelTime = pg.time.get_ticks() - player.channelTime
                        player.jumpRight(min(35, player.channelTime // 10))
                        player.left_flag = False
                        player.right_flag = False
                        player.isChanneling = False
                    elif event.key == pg.K_SPACE:
                        player.channelTime = pg.time.get_ticks() - player.channelTime
                        player.jump(min(35, player.channelTime // 10))
                        player.left_flag = False
                        player.right_flag = False
                        player.isChanneling = False

                    
    def draw(self):
        self.screen.fill((LIGHTBLUE))
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()


    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def find_closest(self, player):
        plat_length = {0: 224, 1: 112, 2: 1200}
        min_distance = WIDTH**2 # to initialize first comparison
        closest_platform = None
        for level in PLATFORM_LIST[player.level: player.level + 2]:
            for plat in level:
                # look only for platforms that are above player
                if HEIGHT * player.level + plat[1] < player.pos.y:
                    # check if platform is on the left or right side of player
                    if plat[0] + plat_length[plat[2]] < player.pos.x: # it's on the left side
                        distance = np.sqrt((player.pos.x - (plat[0] + plat_length[plat[2]]))**2 +\
                                        (player.pos.y - (HEIGHT * player.level + plat[1] + 40))**2)
                    else: # it's on the right side
                        distance = np.sqrt((player.pos.x - plat[0])**2 +\
                                        (player.pos.y - (HEIGHT * player.level + plat[1] + 40))**2)

                    if distance < min_distance:
                        min_distance = distance
                        closest_platform = plat
        # this order is weird but done like this to better fit in AI activation function
        if closest_platform != None:
            return [closest_platform[0], closest_platform[0] + plat_length[closest_platform[2]], closest_platform[1]]
        else:
            None
            
                
if __name__ == '__main__':
    g = Game()
    g.all_sprites = pg.sprite.LayeredUpdates()
    g.platforms = pg.sprite.Group()
    for level in PLATFORM_LIST:
        for plat in level:
            Platform(g, *plat)

    while g.running:
        g.clock.tick(FPS)
        g.player = [Player(g)]
        g.run()

    pg.quit()