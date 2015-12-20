from utils import (deviation_stats, fst, snd, lst, glob_load,
                   get_working_dir, dump, default_input)
from rbn_reservoir_problem import genotype_to_phenotype
from collections import defaultdict
from rbn.rbn_node import RBNNode
from rbn_reservoir_problem import calculate_accuracy
from rbn.complexity_measures import measure_computational_capability
from tasks.temporal import create_datasets

import Oger
import mdp
import numpy as np

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
                                    input_connectivity_range, window_size):
    results = []
    datasets = create_datasets(
        20,
        task_size=200,
        window_size=window_size,
        dataset_type='temporal_parity')
    training_dataset, test_dataset = datasets[:-1], datasets[-1]

    for input_connectivity in input_connectivity_range:
        logging.info('Sampling N={} with L={}.'
                     .format(n_samples, input_connectivity))
        for sample in range(n_samples):
            try:
                reservoir = RBNNode(connectivity=connectivity,
                                    output_dim=n_nodes,
                                    input_connectivity=input_connectivity)
                readout = Oger.nodes.RidgeRegressionNode(
                    input_dim=reservoir.output_dim,
                    output_dim=1)

                flow = mdp.Flow([reservoir, readout], verbose=1)
                flow.train([None, training_dataset])

                accuracy = calculate_accuracy(flow, test_dataset)
                cc = measure_computational_capability(reservoir, 100, window_size)
                result = [input_connectivity, accuracy, cc]
                results.append(result)
                logging.info(result)
            except Exception as e:
                logging.error(e)
                logging.error('Exception occured, Continuing anyways')

    logging.info(results)
    return results


def erb():
    working_dir = get_working_dir()
    log.setup(logging.DEBUG, path=working_dir)

    window_size = default_input('Window size', 3)
    n_nodes = default_input('N Nodes', 100)
    connectivity = default_input('Connectivity', 2)
    f = default_input('From', 0)
    t = default_input('To', n_nodes + 1)
    s = default_input('Step', n_nodes / 10)
    r = range(f, t, s)

    distribution = estimate_reservoir_distribution(
        30, n_nodes, connectivity, r, window_size)

    name = '[NN:{}-WS:{}-K:{}]-distribution'.format(n_nodes, window_size, connectivity)
    dump(distribution, name, folder=working_dir)


def computational_power_scatter(filename):
    with open(filename) as f:
        print "x y"
        for line in f:
            numbers = eval(line)
            print numbers[2], numbers[1]


def distribution_to_plot(filename):
    distribution = {}
    with open(filename) as f:
        for line in f:
            arr = eval(line)
            L = arr[0]
            if not L in distribution:
                distribution[L] = []

            distribution[L].append(arr[1:])

    print "\\myboxplot{"

    for i, l in enumerate(sorted(distribution.keys())):
        values = distribution[l]
        accuracies = map(fst, values)
        complexities = map(snd, values)

        median = np.median(accuracies)
        lowerq = np.percentile(accuracies, 25)
        upperq = np.percentile(accuracies, 75)
        if abs(lowerq - upperq) < 0.001:
            lowerq -= 0.004

        upperw = np.max(accuracies)
        lowerw = np.min(accuracies)

        boxplot =\
"""% L: {}
\\addplot[
boxplot prepared={{
    draw position={},
    median={},
    upper quartile={},
    lower quartile={},
    upper whisker={},
    lower whisker={}
}},
] coordinates {{}};""".format(l, i, median, upperq, lowerq, upperw, lowerw)

        print boxplot

    print "}}{{{}}}".format(10.0 / max(distribution.keys()))


if __name__ == '__main__':
    #filename = "pickle_dumps/distribution-100-5-3/combined-distribution"
    #computational_power_scatter()
    #distribution_to_plot()
    #erb()

    genomes, rbns = load_rbns_from_ea()
    print "% connectivity"
    for rbn in rbns:
        print rbn.input_connectivity

    #deviation_stats('Fitness', [g.fitness for g in genomes])
    #deviation_stats('Input connectivity', [len(rbn.input_connections)
    #                                       for rbn in rbns])

    #print [degree_distribution(rbn) for rbn in rbns]
