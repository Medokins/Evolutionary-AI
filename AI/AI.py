import os
import sys
import neat
from main import *

gen = 0

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
    for plat in PLATFORM_LIST:
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
        for x, player in enumerate(game.player):
            previous_best = player.pos.y
            if player.pos.y > previous_best: 
                ge[x].fitness += 0.1

            hits = pg.sprite.spritecollide(player, game.platforms, False)
            if not hits: 
                player.jumping = True
            else:
                player.jumping = False

            # send player x, y and platforms x start, x end and top y position 
            # closest -> closest platform to player above him yet to implement
            # output = nets[game.player.index(player)].\
            #     activate(player.pos.x, player.pos.y, closest.rect.topleft[0], closest.rect.topright[0], closest.rect.topleft[1])
            # if player.jumping == False:
            #     if output[0] > 0:
            #         player.jumpRight(output[0])
            #     else:
            #         player.jumpLeft(abs(output[0]))

        game.update()
        game.draw()

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
    #p.add_reporter(neat.Checkpointer(5))
    winner = p.run(eval_genomes, 50)


local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward.txt')
run(config_path)