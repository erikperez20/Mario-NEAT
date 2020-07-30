import retro
import cv2
import os
import neat
import numpy as np
import pickle 
import argparse


IMG_SCALE_FACTOR = 8
ENV_NAME = 'SuperMarioBros-Nes'
env = retro.make(game=ENV_NAME, state='Level1-1')

def parse_args():

    parser = argparse.ArgumentParser('NEAT for Super Mario Bros Game')
    parser.add_argument('--config_file', type = str , help = 'Config NEAT filename with hyperparameters data, Ex: config-feedforward')
    parser.add_argument('--generations', type = int , help = 'Number of generations to compute')

    return parser.parse_args()


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        obs = env.reset()
        act = env.action_space.sample()
        inx, iny, inc = env.observation_space.shape
        inx = int(inx/IMG_SCALE_FACTOR)
        iny = int(iny/IMG_SCALE_FACTOR)
        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        
        done = False
        counter = 0
        fitness = 0
        cv2.namedWindow("main", cv2.WINDOW_NORMAL)
        while not done:
            env.render()
            obs = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
            obs = cv2.resize(obs, (inx, iny))
            cv2.imshow('main', obs)
            cv2.waitKey(1)
            imgarray = np.ndarray.flatten(obs)
            act = net.activate(imgarray)
            obs, rew, done, info = env.step(act)
            if rew > 0.0:
                fitness += rew
                counter = 0
            else:
                counter+=1
            genome.fitness = fitness
            if counter == 300:
                done = True
                print(genome_id, fitness)

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    
    p = neat.Population(config)
    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)


    f = open(f'{config_path}_stats_gen_{gen_num}','w+')
    print(f'{config_path}_stats_{gen_num}')

    winner = p.run(eval_genomes, n = gen_num)

    max_fitness = stats.get_fitness_stat(max)
    mean_fitness = stats.get_fitness_mean()
    std_fitness = stats.get_fitness_stdev()
    species_size = stats.get_species_sizes()
    species_fitness = stats.get_species_fitness(null_value = "NA")


    print(len('Generations'))

    f.write('Fitness Statistics\n')
    f.write('Generations' + '     ' + 'Max' + '     ' + 'Mean' + '     ' + 'Standard Deviation' + '\n')
    for i in range(gen_num):
        f.write(str(i) + len('Generations      ')*" "+ str(max_fitness[i])+ len('Max      ')*" " + str(mean_fitness[i]) + \
            len('Mean      ')*" " + str(std_fitness[i]) + "\n")
        # f.write("This is line %d\r\n" % (i+1))

    f.write('Species Statistics\n')
    f.write('Species Sizes\n')

    species_nums = len(species_size[0])
    string_species = ''
    for i in range(species_nums):
        string_species = string_species + f'     Species {i+1}'
    print(string_species)

    f.write('Generations' + string_species + '\n')

    for i in range(gen_num):
        species_nums_string = ''
        for j in species_size[i]:
            species_nums_string = species_nums_string + 5*' ' + str(j)

        print(species_nums_string)
        f.write(str(i) + species_nums_string  + '\n')

    f.write('Species Fitness Mean\n')
    f.write('Generations' + string_species + '\n')

    for i in range(gen_num):
        species_fit_string = ''
        for j in species_fitness[i]:
            species_fit_string = species_fit_string + 5*' ' + str(j)

        f.write(str(i) + species_fit_string  + '\n')

        print(species_fit_string)

    f.close() 

    print('##########')
    print(' Max Fitness in Each Generation: ')
    print(stats.get_fitness_stat(max))
    print(' Mean Fitness in Each Generation: ')
    print(stats.get_fitness_mean())
    print(' Std Fitness in Each Generation: ')
    print(stats.get_fitness_stdev())
    #print(stats.best_genomes(3))
    print(stats.get_species_sizes())
    print(stats.get_species_fitness(null_value = "NA"))
    # stats.save_species_fitness(delimiter = ' ', null_value = 'NA', filename = 'species_fitness1')
    print('##########')



    with open(f"{ENV_NAME}.pkl", "wb") as f:
        pickle.dump(file=f, obj=winner)

if __name__ == "__main__":

    args = parse_args()
    gen_num = args.generations
    path = os.path.join(os.path.dirname(__file__), 'Config_Files' )
    config_path = os.path.join(path, args.config_file)
    run(config_path)
