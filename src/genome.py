import numpy as np
import copy

class Genome():

    @staticmethod
    def get_random_gene(length=10):
        """
        Generates a list of random float values of a given length
        """
        gene = np.array([np.random.random() for i in range(length)])
        return gene

    @staticmethod
    def get_random_genome(gene_length, genome_count):
        """
        Generates a random list of a gene of a determined length, list of lists,
        """
        genome = [Genome.get_random_gene(gene_length) for i in range(genome_count)]
        return genome

    @staticmethod
    def get_gene_spec():
        """
        Lays out the specification for what a gene looks like. allows us to 
        unpack the gene
        """

        spec =  {
                "link-shape": {"scale":1},
                "link-length": {"scale":1},
                "link-radius": {"scale":1},
                "link-recurrence": {"scale":4},
                "lin-mass": {"scale":1},
                "joint-mass":{"scale":1},
                "joint-type":{"scale":1},
                "joint-parent":{"scale":1},
                "joint-axis-ayz":{"scale":1},
                "joint-origin-rpy-1": {"scale":np.pi*2},
                "joint-origin-rpy-2": {"scale":np.pi*2},
                "joint-origin-rpy-3": {"scale":np.pi*2},
                "joint-origin-xyz-1": {"scale":1},
                "joint-origin-xyz-2": {"scale":1},
                "joint-origin-xyz-3": {"scale":1},
                "control-waveform": {"scale":1},
                "control-amp": {"scale":0.25},
                "control-freq": {"scale": 1}
                }

        ind = 0 
        for key in spec.keys():
            spec[key]["ind"] = ind
            ind = ind + 1

        return spec

    @staticmethod
    def expandLinks(parent_link, uniq_parent_name, flat_links, exp_links):
        """
        Recurcivly expand the flat links to indervidual, more like how it will 
        be represented as a graph
        """
        children = [l for l in flat_links if l.parent_name == parent_link.name]
        for c in children:
            for r in range(c.recur):
                c_copy = copy.copy(c)
                c_copy.parent_name = uniq_parent_name
                uniq_name = c_copy.name + str(len(exp_links))
                c_copy.name = uniq_name
                exp_links.append(c_copy)
                Genome.expandLinks(c, uniq_name, flat_links, exp_links)

class URDFLink():
    def __init__(self, name, parent_name, recur):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur

    def phase_two():
        pass
