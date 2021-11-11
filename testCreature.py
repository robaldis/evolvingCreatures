import unittest
from src import creature

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




unittest.main()
