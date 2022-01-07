from simulation import population
from simulation import simulation
from creature import genome
from creature import creature
import numpy as np

# Number of generations
N_GEN = 20

hyper_parameters = {
        'pop_size': 10,
        'gene_count': 3,
        'mutation_rate': 0.1,
        'mutation_range': 0.25
}

# Parameters to test
pop_size = ('pop_size', range(1,20))
gene_count = ('gene_count', range(2,10))
mutation_rate = ('mutation_rate', list(np.arange(0.1, 1, 0.1).round(2)))
mutation_range = ('mutation_rate', list(np.arange(0.1, 1, 0.1).round(2)))

testing_parameters = [pop_size, gene_count, mutation_rate, mutation_range]


def run_ga(hyper_parameters):
    c = creature.Creature(20)

    pop = population.Population(pop_size=hyper_parameters['pop_size'], gene_count=hyper_parameters['gene_count'])
    sim = simulation.ThreadedSim(pool_size= 8)
    parameter = "pop_size"

    fitness = []

    for generation in range(N_GEN):
        sim.eval_population(pop, 2400)
        fit_map = [cr.get_distance_travled() for cr in pop.creatures]
        fmax = np.max(fit_map)
        for cr in pop.creatures:
            if cr.get_distance_travled() == fmax:
                elite = cr
                break

        new_gen = []
        for cid in range(len(pop.creatures)):
            p1_ind = population.Population.select_parent(fit_map)
            p2_ind = population.Population.select_parent(fit_map)
            dna = genome.Genome.crossover(pop.creatures[p1_ind].dna, pop.creatures[p2_ind].dna)

            mutation_rate = 0.1
            mutation_range = 0.25
            dna = genome.Genome.point_mutate(dna, hyper_parameters['mutation_rate'], hyper_parameters['mutation_range'])
            dna = genome.Genome.grow_mutate(dna, 0.25)
            dna = genome.Genome.shrink_mutate(dna, 0.25)
            cr = creature.Creature(1)
            cr.set_dna(dna)
            new_gen.append(cr)

        new_gen[0] = elite
        csv_filename = 'csv/' + str(generation) + '_elite.csv'
        genome.Genome.to_csv(elite.dna, csv_filename)
        pop.creatures = new_gen
        #print(generation, np.max(fit_map), np.mean(fit_map))
        fitness.append(np.mean(fit_map))
    return fitness
        
        
def main():
    with open('parameter_testing.csv', 'w+') as f:
        f.write('generation, mean_fitness, parameter, parameter_value\n')

    print(testing_parameters)
    for parameter in testing_parameters:
        print(f"Parameter being tested: {parameter[0]}")
        for value in parameter[1]:
            print(f"Value being tested: {value}")
            hyper_parameters = {
                    'pop_size': 10,
                    'gene_count': 3,
                    'mutation_rate': 0.1,
                    'mutation_range': 0.25
            }

            hyper_parameters[parameter[0]] = value
            try: 
                fitnesses = run_ga(hyper_parameters)
            except IndexError:
                print("error")
                break

            with open('parameter_testing.csv', 'a+') as f:
                for i, fitness in enumerate(fitnesses):
                    f.write(f'{i}, {fitness}, {parameter[0]}, {value}\n')

if __name__ == "__main__":
    main()
