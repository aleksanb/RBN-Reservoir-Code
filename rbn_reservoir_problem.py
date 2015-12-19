from ea.adult_selection import generational_mixing
from ea.crossover import genome_component_crossover
from ea.mutation import per_genome_component_mutation
from ea.parent_selection import tournament_selection
from ea.problem import Problem

from rbn.rbn_node import RBNNode

import mdp


def genotype_to_phenotype(genotype, n_nodes, connectivity):
    input_connections = []
    connections = []
    rules = []

    for i in range(n_nodes):
        chunk = genotype[i:i+connectivity+2]

        connected = chunk[0] % 2 == 1
        neighbors = chunk[1:1+connectivity]

        rule = chunk[-1] % 2 ** 2 ** connectivity
        rule = ("{:0%db}" % 2 ** connectivity).format(rule)
        rule = map(int, rule)

        if connected:
            input_connections.append(i)

        connections.append(neighbors)
        rules.append(rule)

    return RBNNode(connectivity=connectivity,
                   output_dim=n_nodes,
                   input_connections=input_connections,
                   connections=connections,
                   rules=rules)


def calculate_accuracy(flow, (reservoir_input, expected_output)):
    actual_output = flow.execute(reservoir_input)
    for output in actual_output:
        output[0] = 1 if output[0] > 0.5 else 0

    errors = sum(actual_output != expected_output)
    accuracy = 1 - float(errors) / len(actual_output)

    return accuracy


class RBNReservoirProblem(Problem):
    children_pool_size = 40
    adult_pool_size = 40
    fitness_satisfaction_threshold = 0.98
    maximum_generations = 200

    select_adults = generational_mixing()
    select_parent = tournament_selection(k=8)

    crossover = genome_component_crossover(p=0.5)
    mutate = per_genome_component_mutation(probability=0.1)

    def __init__(self,
                 n_nodes,
                 connectivity,
                 readout,
                 dataset):
        self.n_nodes = n_nodes
        self.connectivity = connectivity
        self.readout = readout
        self.dataset = dataset

        self.genotype_symbol_set_size = n_nodes
        self.problem_size = (connectivity + 2) * n_nodes

        if n_nodes < 2 ** 2 ** connectivity:
            print "n < 2**2**k :("

    def calculate_fitness(self, genotype):
        rbn_reservoir = genotype_to_phenotype(
            genotype, self.n_nodes, self.connectivity)

        rbn_reservoir.reset_state()
        flow = mdp.Flow([rbn_reservoir, self.readout], verbose=1)

        return calculate_accuracy(flow, self.dataset)
