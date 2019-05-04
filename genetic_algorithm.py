"""
Knapsack problem.

Genetic evolutionary algorithm implementation. This is an approximation algorithm
meaning you can't be sure if global optimal solution is found.

"""
import random
import itertools

class Genome(object):
    """ Object holds possible solution to a problem
    """

    def __init__(self):
        self.genes = []
        self.fitness = 0

    def __eq__(self, other):
        return self.genes == other.genes

    def __hash__(self):
        return hash(str(self.genes))

    def init_random(self, n_genes):
        self.genes = [random.randint(0, 1) for _ in range(n_genes)]

    def init_empty(self, n_genes):
        self.genes = [0 for _ in range(n_genes)]

    def __repr__(self):
        return "%d %s" % (self.fitness, str(self.genes))

class KS(object):

    def __init__(self, pop_size=50, n_generations=10):
        self.population = []
        self.pop_size = pop_size
        self.n_generations = n_generations

        self.weights = []
        self.values = []
        self.capacity = 0

        self.n_genes = 0

        self.best_value = 0
        self.best_items = []

        self.known_genomes = {}

    def init_population(self):
        
        n = self.n_genes
        if self.pop_size < self.n_genes:
            n = self.pop_size

        for i in range(n):
            genome = Genome()
            genome.init_empty(n_genes=self.n_genes)
            genome.genes[i] = 1
            self.population.append(genome)

        while len(self.population) < self.pop_size:
            genome = Genome()
            genome.init_random(n_genes=self.n_genes)
            self.population.append(genome)

    def fitness(self, genome):
        """ Calculate fitness score for a given genome

            Args:
                genome (Genome)

            Returns:
                score (int): if all items fit the bag, zero otherwise
        """

        value = 0
        weight = 0

        for index, gene in enumerate(genome.genes):
            if gene:
                weight += self.weights[index]
                value += self.values[index]

        if weight > self.capacity:
            # Items are too heavy
            value = 0

        return value

    def selection(self):
        """ Do selection on population.
            Calculate fitness score and sort
        """

        # Calculate fitness score
        for p in self.population:

            _p = self.known_genomes.get(hash(p), None)

            if _p:
                p.fitness = _p.fitness
            else:
                p.fitness = self.fitness(p)
                self.known_genomes[hash(p)] = p

        # Sort by best fitness score
        self.population = sorted(
                self.population, key=lambda x: x.fitness, reverse=True)

        best = self.population[0]

        if self.best_value < best.fitness:
            self.best_value = best.fitness
            self.best_items = best.genes

    def crossover(self, parent1, parent2):
        """ Breed two given parent genomes and return offspring

            Args:
                parent1 (Genome)
                parent2 (Genome)
            Returns:
                offspring (Genome)
        """

        offspring = Genome()
        offspring.init_empty(n_genes=self.n_genes)

        for i in range(self.n_genes):
            offspring.genes[i] = random.choice([parent1.genes[i], parent2.genes[i]])

        # mutate
        i = random.randint(0, self.n_genes-1)
        offspring.genes[i] = random.randint(0, 1)

        return offspring

    def optimize(self, weights, values, capacity, expected=None):
        """ Run GA to maximize item value which fit into knapsack
        """

        if len(weights) != len(values):
            print("List of weights and values have different length")
            return

        if capacity < 1:
            print("Capacity should be more than 0")
            return

        self.weights = weights
        self.values = values
        self.n_genes = len(weights)
        self.capacity = capacity

        self.init_population()

        for i in range(1, self.n_generations+1):
            print("Generation", i)

            # Selection. Evaluate all solutions and sort them
            self.selection()

            for p in self.population[:3]:
                print(p.fitness)

            if expected and expected == self.population[0].fitness:
                # Found best solution, stopping
                break

            # Create new generation from best parents
            next_generation = []

            # Create all possible combinations of parents
            parents = itertools.combinations(self.population, 2)

            # Sort parents by the sum of fitness score
            parents = sorted(parents, key=lambda x: sum(n.fitness for n in x), reverse=True)
            
            # Add best parents to next generation
            for parent in self.population[:25]:
                if parent.fitness <=0:
                    continue
                    
                # do not add duplicates
                if parent not in next_generation:
                    next_generation.append(parent)

            # Create offsprings using crossover of two parents
            for (parent1, parent2) in parents:
                # Both parents with zero fitness are worthless. One is fine
                if parent1.fitness <= 0 and parent2.fitness <= 0:
                    continue

                offspring = self.crossover(parent1, parent2)

                # Do not add duplicate offsprings
                if offspring not in next_generation:
                    next_generation.append(offspring)

                if len(next_generation) >= self.pop_size:
                    # Population is full
                    break

            # If population is not full then fill it with random solutions
            while len(next_generation) < self.pop_size:
                genome = Genome()
                genome.init_random(n_genes=self.n_genes)
                next_generation.append(genome)

            # Add 25 new and random solutions
            for _ in range(25):
                genome = Genome()
                genome.init_random(n_genes=self.n_genes)
                next_generation.append(genome)

            self.population = next_generation

if __name__ == "__main__":

    import json

    with open("dataset.json", "r") as f:
        data = json.load(f)

    n = 25
    w = data["weights"][:n]
    v = data["values"][:n]
    c = data["capacities"][n]

    ks = KS(pop_size=1000, n_generations=100)
    ks.optimize(w, v, c, expected=data["bests"][n])

    print("Best: ", ks.best_value, "| Expected:", data["bests"][n])
