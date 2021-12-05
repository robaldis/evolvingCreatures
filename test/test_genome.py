import unittest
from creature import genome
import numpy as np
from xml.dom.minidom import getDOMImplementation
import os

class GenomeTest(unittest.TestCase):

    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)

    def testRandomeGene(self):
        self.assertIsNotNone(genome.Genome.get_random_gene())

    def testRandomGeneNotNone(self):
        self.assertIsNotNone(genome.Genome.get_random_gene())

    def testRandomGeneLength(self):
        gene = genome.Genome.get_random_gene(10)
        self.assertEqual(len(gene), 10)

    def testRandGeneIsNumpyArrays(self):
        gene = genome.Genome.get_random_gene(10)
        self.assertEqual(type(gene), np.ndarray)

    def testRandomGenomeExists(self):
        data = genome.Genome.get_random_genome(10,5)
        self.assertIsNotNone(data)


    def testGeneSpecExists(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec)

    def testGeneSpecHasLinkLength(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length'])

    def testGeneSpecHasLinkLengthIndex(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length']['ind'])

    def testGeneSpecLength(self):
        spec = genome.Genome.get_gene_spec()
        self.assertEqual(len(spec), 18)


    def testGeneSpecScale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        self.assertGreater(gene[spec['link-length']['ind']], 0)


    def testFlatLinks(self):
        links = [
                genome.URDFLink(name="A", parent_name=None, recur=1),
                genome.URDFLink(name="B", parent_name="A", recur=1),
                genome.URDFLink(name="C", parent_name="B", recur=2),
                genome.URDFLink(name="D", parent_name="C", recur=1)
                ]
        self.assertIsNotNone(links)


    def testExpandLinksLen(self):
        links = [
                genome.URDFLink(name="A", parent_name=None, recur=1),
                genome.URDFLink(name="B", parent_name="A", recur=1),
                genome.URDFLink(name="C", parent_name="B", recur=2),
                genome.URDFLink(name="D", parent_name="C", recur=1)
                ]
        exp_links = [links[0]]
        genome.Genome.expand_links(links[0], links[0].name, links, exp_links)
        names = [l.name + " " + str(l.parent_name) for l in exp_links]
        # print(names)
        self.assertEqual(len(exp_links), 6)

    def testExpandLinksEqual(self):
        links = [
                genome.URDFLink(name="A", parent_name=None, recur=1),
                genome.URDFLink(name="B", parent_name="A", recur=1),
                genome.URDFLink(name="C", parent_name="B", recur=2),
                genome.URDFLink(name="D", parent_name="C", recur=1)
                ]
        expected = ["A", "B1", "C2", "D3", "C4", "D5"]
        exp_links = [links[0]]
        genome.Genome.expand_links(links[0], links[0].name, links, exp_links)
        names = [l.name for l in exp_links]
        self.assertEqual(names, expected)


    def testGeneToGenomeDict(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(len(spec))
        gene_dict = genome.Genome.get_gene_dict(gene, spec)
        self.assertIn("joint-parent", gene_dict)

    def testGenomeToDictLength(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        gene_dicts = genome.Genome.get_genome_dict(dna, spec)
        self.assertEqual(len(gene_dicts), 3)

    def testGetLinks(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        dna_dict = genome.Genome.get_genome_dict(dna, spec)
        links = genome.Genome.genome_to_links(dna_dict)
        self.assertEqual(len(links), 3)
        
    def testLinkToXMLNotNone(self):
        link = genome.URDFLink(name="A", parent_name=None, recur=1)
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "robot", None)
        xml = link.to_link_element(adom)
        self.assertIsNotNone(xml)

    def testJointToXMLNotNone(self):
        link = genome.URDFLink(name="A", parent_name="A", recur=1)
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "robot", None)
        xml = link.to_joint_element(adom)
        self.assertIsNotNone(xml)

    def testCrossover(self):
        g1 = [[1,1,1], [2,2,2], [3,3,3]]
        g2 = [[4,4,4], [5,5,5], [6,6,6]]
        for i in range(100):
            g3 = genome.Genome.crossover(g1, g2)
            self.assertGreater(len(g3), 0)

    def testPointMutate(self):
        g1 = [[1.,1.,1.], [2.,2.,2.], [3.,3.,3.]]
        # print(g1)
        g2 = genome.Genome.point_mutate(g1, rate=0.5, amount=0.25)
        # print(g2)

    def testShrinkMutate(self):
        g1 = [[1.,1.,1.], [2.,2.,2.], [3.,3.,3.]]
        g2 = genome.Genome.shrink_mutate(g1, rate=1)
        self.assertNotEqual(len(g1), len(g2))

    def testGrow(self):
        g1 = [[1.,1.,1.], [2.,2.,2.], [3.,3.,3.]]
        g2 = genome.Genome.grow_mutate(g1, rate=1)
        self.assertGreater(len(g2), len(g1))

    def test_tocsv(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, 'test.csv')
        self.assertTrue(os.path.exists('test.csv'))

    def test_tocsv2(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, 'test.csv')
        expect = "1,2,3,\n"
        with open("test.csv", "r") as f:
            csv_str = f.read()
            f.close()
        self.assertEqual(csv_str, expect)

    def test_fromcsv(self):
        g1 = [[1,2,3], [4,5,6]]
        genome.Genome.to_csv(g1, 'test.csv')
        g2 = genome.Genome.from_csv('test.csv')
        print(g1, g2)
        self.assertEqual(g1, g2)
        


    

if __name__ == "__main__":
    unittest.main()
