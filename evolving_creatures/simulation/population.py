from creature import creature


class Population:
    def __init__(self, pop_size=1, gene_count=3):
        self.creatures = [creature.Creature(gene_count) for size in range(pop_size)]




