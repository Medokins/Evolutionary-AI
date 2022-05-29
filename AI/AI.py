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
    gen += 1

    game = Game()
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

    while game.running and len(game.player) > 0:
        game.clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.running = False
                pg.quit()
                sys.exit()
                
        #TO DO
        for _, player in enumerate(game.player):

            hits = pg.sprite.spritecollide(player, game.platforms, False)
            if not hits: 
                player.jumping = True
            else:
                player.jumping = False

            closest = game.find_closest(player)
            # send player x, y and platforms x start, x end and top y position 
            # closest -> closest platform to player above him
            # closest[0] -> left side, closest[1] -> right side closest[2] -> height 
            # need to change activation function in config file
            # player.pos.x, player.pos.y, closest[0], closest[1], closest[2]
            output = nets[game.player.index(player)].activate((player.pos.x, player.pos.y, closest[0]))
            if player.jumping == False:
                if output[0] > 0:
                    player.jumpRight(output[0])
                else:
                    player.jumpLeft(abs(output[0]))

        game.update()
        game.draw(player, closest)

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play jumo king.
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