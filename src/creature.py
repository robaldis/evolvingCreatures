from src import genome

class Creature():
    def __init__(self, gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)
        pass

    def get_flat_links(self):
        gdict = genome.Genome.get_genome_dict(self.dna, self.spec)
        self.flat_links = genome.Genome.genome_to_links(gdict)
        return self.flat_links

    def get_expanded_links(self):
        self.get_flat_links()
        exp_links = []
        genome.Genome.expandLinks(self.flat_links[0], self.flat_links[0].name, self.flat_links, exp_links)

        return exp_links

    def to_xml(self):
        pass
