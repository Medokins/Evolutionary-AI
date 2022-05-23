import pygame as pg 
from settings import *
from sprites import *
from os import path

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

        self.channelTime = 0
        self.isChanneling = False
        self.left_flag = False
        self.right_flag = False

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try: self.highscore = int(f.read())
            except: self.highscore = 0

        # load images
        img_dir = path.join(self.dir, 'Images')            

        # load platform images
        self.spritesheet = [Spritesheet(path.join(img_dir, "platforms", "platform_1.png")),
                            Spritesheet(path.join(img_dir, "platforms", "platform_2.png")),
                            Spritesheet(path.join(img_dir, "platforms", "ground.png"))]

        # load character images
        self.character_standing = [
                                Spritesheet(path.join(img_dir, "standing", "standing1.png")),\
                                Spritesheet(path.join(img_dir, "standing", "standing2.png")),\
                                Spritesheet(path.join(img_dir, "standing", "standing3.png"))
                                ]

        # load sounds
        self.sound_dir = path.join(self.dir, 'sound')


    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)

        for plat in PLATFORM_LIST:
            Platform(self, *plat)

        self.run()

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
        self.all_sprites.update(self.isChanneling)

        # if player reaches top 1/4 of screen
        if self.player.rect.top < HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    self.score += 10

        # if player reaches bottom 7/10 of screen
        if self.player.rect.top > HEIGHT * 7/10:
            self.player.pos.y -= max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y -= max(abs(self.player.vel.y), 2)
        
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            #print(f"Player pos: {self.player.pos.x}, platform: {hits[0].rect.bottomleft[0]}")
            # top platform colision
            if self.player.vel.y > 0:
                if self.player.pos.x -5 > hits[0].rect.topleft[0] and self.player.pos.x + 5 < hits[0].rect.topright[0]:
                    if self.player.pos.y > hits[0].rect.top and self.player.pos.y < hits[0].rect.bottom:
                        self.player.pos.y = hits[0].rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

            # bottom platform colision
            elif self.player.vel.y < 0:
                if self.player.pos.x >= hits[0].rect.bottomleft[0] and self.player.pos.x <= hits[0].rect.bottomright[0]:
                    if self.player.pos.y - self.player.rect[1] <= hits[0].rect.top:
                        self.player.vel.y = 0

            # bouncing off sides
            if self.player.pos.x + 30 < hits[0].rect.bottomleft[0] or self.player.pos.x - 30 > hits[0].rect.bottomright[0]:
                if self.player.jumping:
                    self.player.vel.x = -self.player.vel.x 
                    
    def events(self):
        
        # Game Loop - events
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if not hits: self.player.jumping = True
        else: self.player.jumping = False

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
                    self.player.jump_height = min(35, self.channelTime // 10)
                    self.player.jumpLeft()
                    self.left_flag = False
                    self.right_flag = False
                    self.isChanneling = False
                elif event.key == pg.K_SPACE and self.right_flag:
                    self.channelTime = pg.time.get_ticks() - self.channelTime
                    self.player.jump_height = min(35, self.channelTime // 10)
                    self.player.jumpRight()
                    self.left_flag = False
                    self.right_flag = False
                    self.isChanneling = False
                elif event.key == pg.K_SPACE:
                    self.channelTime = pg.time.get_ticks() - self.channelTime
                    self.player.jump_height = min(35, self.channelTime // 10)
                    self.player.jump()
                    self.left_flag = False
                    self.right_flag = False
                    self.isChanneling = False

    def draw(self):
        self.screen.fill((LIGHTBLUE))
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(LIGHTBLUE)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(LIGHTBLUE)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()