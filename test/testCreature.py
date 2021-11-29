import unittest
from creature import creature

class TestCreature (unittest.TestCase):

    def testCreatureExists(self):
        self.assertIsNotNone(creature.Creature)
    
    def testGetFlatLinks(self):
        c = creature.Creature(gene_count=4)
        links = c.get_flat_links()
        self.assertEqual(len(links), 4)

    def testGetExpandedLinks(self):
        for i in range(100):
            c = creature.Creature(gene_count=25)
            links = c.get_flat_links()
            exp_links = c.get_expanded_links()
            self.assertGreaterEqual(len(exp_links), len(links))


    def testToXML(self):
        c = creature.Creature(gene_count=4)
        xml = c.to_xml()
        self.assertIsNotNone(xml)

    def testUpdateDistanceStartPos(self):
        c = creature.Creature(gene_count=4)
        c.update_position((0,0,0))
        self.assertIsNotNone(c.start_pos)

    def testUpdateDistanceLastPos(self):
        c = creature.Creature(gene_count=4)
        c.update_position((0,0,0))
        c.update_position((1,0,0))
        c.update_position((2,0,0))
        c.update_position((3,0,0))
        self.assertIsNotNone(c.last_pos)

    def testGetDistanceLastPos(self):
        c = creature.Creature(gene_count=4)
        c.update_position((0,0,0))
        c.update_position((1,0,0))
        c.update_position((2,0,0))
        c.update_position((3,0,0))
        dist = c.get_distance_travled()
        self.assertEqual(dist, 3)

    def testGetDistanceNoTravel(self):
        c = creature.Creature(gene_count=4)
        dist = c.get_distance_travled()
        self.assertEqual(dist, 0)

if __name__ == "__main__":
    unittest.main()
