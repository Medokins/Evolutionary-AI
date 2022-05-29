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
        self.player = [Player(self)]

        for level in PLATFORM_LIST:
            for plat in level:
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
        self.all_sprites.update()

        highest_player = self.player[0]
        highest = self.player[0].pos.y
        for player in self.player:
            if player.pos.y <= highest:
                highest_player = player

                #if at top of screen
                if highest_player.rect.top < 0:
                    player.pos.y += HEIGHT
                    for plat in self.platforms:
                        plat.rect.y += HEIGHT

                #if player reaches bottom of screen
                if highest_player.rect.top > HEIGHT:
                    player.pos.y -= HEIGHT
                    for plat in self.platforms:
                        plat.rect.y -= HEIGHT
            
            hits = pg.sprite.spritecollide(player, self.platforms, False)
            if hits:
                #print(f"Player pos: {self.player.pos.x}, platform: {hits[0].rect.bottomleft[0]}")
                # top platform colision
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
                    
    def events(self):
        
        # Game Loop - events
        for player in self.player:
            hits = pg.sprite.spritecollide(player, self.platforms, False)
            if not hits:
                player.jumping = True
            else:
                player.jumping = False

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False

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
                        player.jump_height = min(35, player.channelTime // 10)
                        player.jumpLeft()
                        player.left_flag = False
                        player.right_flag = False
                        player.isChanneling = False
                    elif event.key == pg.K_SPACE and player.right_flag:
                        player.channelTime = pg.time.get_ticks() - player.channelTime
                        player.jump_height = min(35, player.channelTime // 10)
                        player.jumpRight()
                        player.left_flag = False
                        player.right_flag = False
                        player.isChanneling = False
                    elif event.key == pg.K_SPACE:
                        player.channelTime = pg.time.get_ticks() - player.channelTime
                        player.jump_height = min(35, player.channelTime // 10)
                        player.jump()
                        player.left_flag = False
                        player.right_flag = False
                        player.isChanneling = False

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
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()

    pg.quit()