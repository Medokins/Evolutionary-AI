import os
import sys
import neat
from main import *

gen = 0
DRAW_LINES = True

def eval_genomes(genomes, config):
    """
    runs the simulation of the current population of
    players and sets their fitness based on the height they
    reach in the game.
    """
    global gen
    best_moves = []
    gen += 1

    game = Game(AI = True)
    game.all_sprites = pg.sprite.LayeredUpdates()
    game.platforms = pg.sprite.Group()
    for level in PLATFORM_LIST:
        for plat in level:
            Platform(game, *plat)

    nets = []
    ge = []

    for _, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game.player.append(Player(game))
        nets.append(net)
        ge.append(genome)

    max_level = 0
    iter = 0

    while game.running and len(game.player) > 0:
        game.clock.tick(FPS)
        iter += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.running = False
                pg.quit()
                sys.exit()
                
        for x, player in enumerate(game.player):
            # if any player exceed current level kill all other players:
            if player.level > max_level:
                max_level = player.level
                best_moves.append(player.jumps)

            hits = pg.sprite.spritecollide(player, game.platforms, False)
            if hits and player.vel.y >= 0: 
                player.jumping = False
            else:
                player.jumping = True


            if not player.jumping:
                closest = game.find_closest(player)
                # closest -> closest platform to player above him
                # closest[0] -> left side, closest[1] -> right side. closest[2] -> height

                if closest != None:
                    distance_left = player.pos.x - closest[0]
                    distance_right = player.pos.x - closest[1]
                    distance_y = player.pos.y - closest[2]
                    output = nets[game.player.index(player)].activate((distance_left, distance_right, distance_y))

                    if output[0] > 0:
                        player.jumpRight(output[0])
                    elif output[0] < 0:
                        player.jumpLeft(abs(output[0]))

                else:
                    player.jump(999)
                    best_moves.append([999])
                    print("GAME OVER")
                    level = 1
                    with open('best.txt', 'w') as f:
                        for array in best_moves:
                            if level != 1:
                                f.write("\n")
                            f.write(f"Level: {level}\n")
                            level += 1
                            for move in array:
                                f.write(str(move))
                                f.write(" ")

            if player.moves == 0 or (player.level < max_level and not player.jumping):
                #print(f"Killed play: {game.player.index(player)} at level {player.level}")
                player.kill()
                game.player.pop(game.player.index(player))

            try:
                if player.highest_platform > player.previous_highest_platform:
                    player.previous_highest_platform = player.highest_platform
                    ge[x].fitness += 10
            except:
                pass

        if iter%100 == 0:
            print(20*"#")        
            print(f"Players left: {len(game.player)}")

        game.update()
        game.draw()

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play jump king.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))
    winner = p.run(eval_genomes, 50)


local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward.txt')
run(config_path)