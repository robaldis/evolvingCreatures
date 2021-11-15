import unittest
from simulation import simulation
from creature import creature
from simulation import population


class TestSim(unittest.TestCase):

        def testSimExists(self):
            sim = simulation.Simulation()
            self.assertIsNotNone(sim)

        def testSimId(self):
            sim = simulation.Simulation()
            self.assertIsNotNone(sim.physicsClientId)

        def testRun(self):
            sim = simulation.Simulation()
            # cr = creature.Creature(gene_count = 3)
            self.assertIsNotNone(sim.run_creature)

        def testPos(self):
            sim = simulation.Simulation()
            cr = creature.Creature(gene_count = 3)
            sim.run_creature(cr)
            self.assertNotEqual(cr.start_pos, cr.last_pos)





if __name__ == "__main__":
    unittest.main()

