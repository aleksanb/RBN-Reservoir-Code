from utils import (deviation_stats, fst, lst, glob_load,
                   get_working_dir, dump, default_input)
from narma30_rbn import create_dataset
from rbn_reservoir_problem import genotype_to_phenotype
from collections import defaultdict
from rbn.rbn_node import RBNNode
from rbn_reservoir_problem import calculate_accuracy
from rbn.complexity_measures import measure_computational_capability

import Oger
import mdp

import log
import logging


def load_rbns_from_ea():
    working_dir = get_working_dir()
    ea_runs = map(fst, glob_load(working_dir + '*-evolved'))

    best_genomes = map(lst, ea_runs)
    rbns = [genotype_to_phenotype(genome, 100, 2)
            for genome in best_genomes]

    return best_genomes, rbns


def degree_distribution(rbn):
    node_indegrees = defaultdict(int)
    for from_node, to_node in rbn.connections:
        node_indegrees[to_node] += 1

    degree_distribution = defaultdict(int)
    for indegree in node_indegrees.values():
        degree_distribution[indegree] += 1

    return degree_distribution


def estimate_reservoir_distribution(n_samples, n_nodes, connectivity,
                                    input_connectivity_range, datasets):
    results = []
    training_dataset, test_dataset = datasets[:-1], datasets[-1]

    for input_connectivity in input_connectivity_range:
        logging.info('Sampling N={} with L={}.'
                     .format(n_samples, input_connectivity))
        for sample in range(n_samples):

            reservoir = RBNNode(connectivity=connectivity,
                                output_dim=n_nodes,
                                input_connectivity=input_connectivity)
            readout = Oger.nodes.RidgeRegressionNode(
                input_dim=reservoir.output_dim,
                output_dim=1)

            flow = mdp.Flow([reservoir, readout], verbose=1)
            try:
                flow.train([None, training_dataset])
            except Exception, e:
                logging.error(e)
                logging.error('Continuing anyways')

            accuracy = calculate_accuracy(flow, test_dataset)
            cc = measure_computational_capability(reservoir, 100, 3)
            result = [input_connectivity, accuracy, cc]
            results.append(result)
            logging.info(result)

    logging.info(results)
    return results


if __name__ == '__main__':
    working_dir = get_working_dir()
    log.setup(logging.DEBUG, path=working_dir)

    window_size = default_input('Window size', 3)
    n_nodes = default_input('N Nodes', 100)

    datasets, descr = create_dataset()
    distribution = estimate_reservoir_distribution(
        30, n_nodes, 2, range(0, n_nodes + 1, n_nodes / 10), datasets)

    name = descr + '-[{}]-distribution'.format(n_nodes)
    dump(distribution, name, folder=working_dir)

    #genomes, rbns = load_rbns_from_ea()

    #deviation_stats('Fitness', [g.fitness for g in genomes])
    #deviation_stats('Input connectivity', [len(rbn.input_connections)
    #                                       for rbn in rbns])

    #print [degree_distribution(rbn) for rbn in rbns]
