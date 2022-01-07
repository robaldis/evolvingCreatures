from creature import creature
import numpy as np


class Population:
    def __init__(self, pop_size=1, gene_count=3):
        self.creatures = [creature.Creature(gene_count) for _ in range(pop_size)]

    @staticmethod
    def get_fitness_map(fitness):
        """
        takes in an array of fitness values (float[]) and returns a map (float[])
        where each value is the sum of all values before it
        """
        fitness_map = []
        running_total = 0
        for value in fitness:
            running_total += value
            fitness_map.append(running_total)

        return fitness_map


    @staticmethod
    def select_parent(fitmap):
        """
        return the index of the one of the parents in the fitness map based on 
        the roulete wheel aproach
        """
        r = np.random.random()
        r *= fitmap[-1]
        for i in range(len(fitmap)):
            if r <= fitmap[i]:
                return i
