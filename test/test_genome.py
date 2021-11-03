import unittest

class GenomeTest (unittest.TestCase):

    def testClassExists(self):
        self.assertIsNotNone(gnome.Genome)
