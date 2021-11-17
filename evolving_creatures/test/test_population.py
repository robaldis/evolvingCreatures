import unittest
from simulation import simulation
from simulation import population
import time

class TestPopulation(unittest.TestCase):

    def testPopExists(self):
        pop = population.Population(pop_size=10, gene_count=3)
        self.assertIsNotNone(pop)

    def testPopHasIndis(self):
        pop = population.Population(pop_size=10, gene_count=3)
        self.assertEqual(len(pop.creatures), 10)

    def testPop(self):
        start = time.time()
        pop = population.Population(pop_size=2, gene_count=3)
        sim = simulation.Simulation()
        for cr in pop.creatures:
            sim.run_creature(cr)
        dists = [cr.get_distance_travled() for cr in pop.creatures]
        # print(dists)

        # print("Single-threading time: " + str(time.time() - start))
        self.assertIsNotNone(dists)

    def testProc(self):
        start = time.time()
        pop = population.Population(pop_size=20, gene_count=3)
        tsim = simulation.ThreadedSim(pool_size=12)
        tsim.eval_population(pop, 2400)
        dists = [cr.get_distance_travled() for cr in pop.creatures]
        # print(dists)
        # print("Mult-threading time: " + str(time.time() - start))
        self.assertIsNotNone(dists)

    def testFitmap(self):
        fits = [2.5, 1.2, 3.4]
        wants = [2.5, 3.7, 7.1]
        fitmap = population.Population.get_fitness_map(fits)
        self.assertEqual(fitmap, wants)

    def testSelPar(self):
        fits = [2.5, 1.2, 3.4]
        fitmap = population.Population.get_fitness_map(fits)
        pid = population.Population.select_parent(fitmap)
        self.assertLess(pid,3)

    def testSelPar2(self):
        fits = [0, 1000, 0.1]
        fitmap = population.Population.get_fitness_map(fits)
        pid = population.Population.select_parent(fitmap)
        self.assertEqual(pid,1)
