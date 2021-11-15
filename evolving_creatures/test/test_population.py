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
        pop = population.Population(pop_size=20, gene_count=3)
        sim = simulation.Simulation()
        for cr in pop.creatures:
            sim.run_creature(cr)
        dists = [cr.get_distance_travled() for cr in pop.creatures]
        print(dists)

        print("Single-threading time: " + str(time.time() - start))
        self.assertIsNotNone(dists)

    def testProc(self):
        start = time.time()
        pop = population.Population(pop_size=20, gene_count=3)
        tsim = simulation.ThreadedSim(pool_size=12)
        tsim.eval_population(pop, 2400)
        dists = [cr.get_distance_travled() for cr in pop.creatures]
        print(dists)
        print("Mult-threading time: " + str(time.time() - start))
        self.assertIsNotNone(dists)

