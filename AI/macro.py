import sys
from main import *

with open("best.txt") as f:
    lines = f.readlines()

iter = 0
instruction = []
for line in lines:
    iter += 1
    if iter%2==0:
        instruction += [int(x) for x in line.split()]

def run_macro(macro):
    print(f"Running macro {macro}\n")
    current_move = 0
    game = Game(AI = False)
    game.all_sprites = pg.sprite.LayeredUpdates()
    game.platforms = pg.sprite.Group()
    for level in PLATFORM_LIST:
        for plat in level:
            Platform(game, *plat)

    game.player = [Player(game, AI=True)]

    while game.running and len(game.player) > 0:
        game.clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.running = False
                pg.quit()
                sys.exit()

        for player in game.player:
            hits = pg.sprite.spritecollide(player, game.platforms, False)
            if hits and player.vel.y >= 0: 
                player.jumping = False
            else:
                player.jumping = True
            
            if not player.jumping:
                if pg.time.get_ticks()%(1.2*player.cooldown) < 15:
                    move = macro[current_move]
                    current_move += 1
                    if move == 999:
                        player.jump(move)
                        print("finish")
                    elif move > 0:
                        player.jumpRight(move)
                        print(f"Jumped right [{move}] (Moves left: {len(macro) - current_move})")
                    elif move < 0:
                        player.jumpLeft(abs(move))
                        print(f"Jumped left [{move}] (Moves left: {len(macro) - current_move})")
        game.update()
        game.draw() 

run_macro(instruction)