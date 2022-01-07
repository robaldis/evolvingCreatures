from simulation import population
from simulation import simulation
from creature import genome
from creature import creature
import numpy as np

# Number of generations
N_GEN = 20

# Parameters to test
pop_size = {'pop_size': range(1,20)}
gene_count = {'gene_count': range(1,10)}
#mutation_rate = range(0.1, 1)
#mutation_range = range(0.1, 1)

testing_parameters = [pop_size, gene_count]

control_pop_size = 10
control_gene_count = 3
control_mutation_rate = 0.1
control_mutation_range = 0.25

for hyper_parameter in testing_parameters:
    
    for value in hyper_parameter:
        pass

c = creature.Creature(20)

pop = population.Population(pop_size=10, gene_count=3)
sim = simulation.ThreadedSim(pool_size= 12)


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
        dna = genome.Genome.point_mutate(dna, mutation_rate, mutation_range)
        dna = genome.Genome.grow_mutate(dna, 0.25)
        dna = genome.Genome.shrink_mutate(dna, 0.25)
        cr = creature.Creature(1)
        cr.set_dna(dna)
        new_gen.append(cr)

    new_gen[0] = elite
    csv_filename = 'csv/' + str(generation) + '_elite.csv'
    genome.Genome.to_csv(elite.dna, csv_filename)
    pop.creatures = new_gen
    print(generation, np.max(fit_map), np.mean(fit_map))
    with open('parameter_testing.csv', 'a+') as f:
        f.write(f'{generation}, {np.mean(fit_map)}, {parameter}\n')
    







