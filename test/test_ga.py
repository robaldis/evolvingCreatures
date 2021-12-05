import unittest
from simulation import population
from simulation import simulation
from creature import genome
from creature import creature
import numpy as np

class TestGA(unittest.TestCase):
    def testBasicGA(self):
        pop = population.Population(pop_size=10, 
                gene_count=3)
        sim = simulation.ThreadedSim(pool_size=8)
        sim.eval_population(pop, 2400)
        fits = [cr.get_distance_travled() for cr in pop.creatures]
        fit_map = population.Population.get_fitness_map(fits)
        new_creatures = []
        for i in range(len(pop.creatures)):
            p1_ind = population.Population.select_parent(fit_map)
            p2_ind = population.Population.select_parent(fit_map)
            p1 = pop.creatures[p1_ind]
            p2 = pop.creatures[p2_ind]
            self.assertIsNotNone(p1)
            self.assertIsNotNone(p2)


        self.assertNotEqual(fits[0], 0)

    def testGA(self):
        pop = population.Population(pop_size=10, gene_count=3)
        sim = simulation.ThreadedSim(pool_size= 12)
        for generation in range(20):
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
                dna = genome.Genome.point_mutate(dna, 0.1, 0.25)
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





if __name__ == "__main__":
    unittest.main()
