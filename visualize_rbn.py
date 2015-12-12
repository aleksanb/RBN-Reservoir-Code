from tasks import temporal
import matplotlib.pyplot as plt
import networkx as nx
from utils import *
import numpy as np
import json

from rbn_reservoir_problem import genotype_to_phenotype
from itertools import repeat

import log
import logging

log.setup(logging.DEBUG)

def visualize_rbn(rbn):
    internal_edges = []
    for i, neighbors in enumerate(rbn.connections):
        internal_edges += zip(repeat(i), neighbors)

    input_edges = zip(repeat('input_node'), rbn.input_connections)

    print input_edges
    print internal_edges

    G = nx.MultiGraph()
    pos = nx.spring_layout(G)

    #G.add_edges_from(internal_edges, node_color='r', node_size=10)
    #G.add_edges_from(input_edges, node_color='b', node_size=3)

    nx.draw_networkx_nodes(G, pos,
                           nodelist=range(rbn.n_nodes),
                           node_color='b',
                           node_size=500,
                           alpha=0.8)

    nx.draw_networkx_edges(G, pos,
                           edgelist=internal_edges)
                           #width=3,
                           #edge_color='r')

#nx.draw_networkx_edges(G,pos,
                               #edgelist=[(0,1),(1,2),(2,3),(3,0)],
                                                      #width=8,alpha=0.5,edge_color='r')
    #nx.draw(G, pos)

    plt.show()


def deviation_stats(description, numbers):
    logger.info('Stats for {}'.format(description))
    logger.info(
        'Largest: {}, Smallest: {}, Mean: {}, Std: {}'
        .format(max(numbers), min(numbers), np.mean(numbers), np.std(numbers)))


def load_rbns_from_ea():
    working_dir = get_working_dir()
    ea_runs = map(fst, glob_load(working_dir + '*-evolved'))

    #genotypes = load('Select EA run: ', folder=working_dir)
    #genotypes = pickle.load(
    #    open('pickle_dumps/chosen-1/2015-12-11-22:59:09-[temporal_parity-10-200-3]-[N:100-K:2]-[TOP:[0.995, 0.995, 0.92]-MEAN:0.609875-STD:0.171931990551-GEN:32]', 'r'))

    best_genomes = map(lst, ea_runs)
    rbns = [genotype_to_phenotype(genome, 100, 2)
            for genome in best_genomes]

    deviation_stats('Fitness', [g.fitness for g in best_genomes])
    deviation_stats('Input connectivity', [len(rbn.input_connections) for rbn in rbns])

    #min_fitness = 0.98  # default_input('Filter criteria:', 0.98)
    #rbns = [genotype_to_phenotype(g, 100, 2)
    #        for g in genotypes
    #        if g.fitness >= min_fitness]

    #visualize_rbn(rbns[-1])


def visualize_dataset(n=30):
    working_dir = get_working_dir()

    test_dataset, filename = glob_load(working_dir + '*-dataset')

    plt.matshow(test_dataset[0][:n], cmap=plt.cm.gray)
    plt.title(filename + ': reservoir input.')

    plt.matshow(test_dataset[1][:n], cmap=plt.cm.gray)
    plt.title(filename + ': expected output.')

    plt.show()


def plot_fitness():
    with open('state.dat', 'r') as states:
        plots = []
        for line in states.readlines():
            state = json.loads(line)
            print state['generation']
            #print line
            #            'children': map(lambda x: x.serialize(), children),
            #            'adults': map(lambda x: x.serialize(), adults),
            #            'generation': generation,
            #            'time': arrow.utcnow().isoformat(),


load_rbns_from_ea()
#visualize_dataset()

#if __name__ == '__main__':
#    plot_fitness()
#    import sys
#    sys.exit()
#
#    # Create datasets
#    dataset_type = default_input('Dataset [temporal_parity, temporal_density]',
#                                 'temporal_parity')
#    n_datasets = default_input('Datasets', 10)
#    task_size = default_input('Dataset length', 200)
#    window_size = default_input('Window size', 3)
#
#    datasets = temporal.create_datasets(
#        n_datasets,
#        task_size=task_size,
#        window_size=window_size,
#        dataset_type=dataset_type)
#    training_dataset, test_dataset = datasets[:-1], datasets[-1]
#
#    dataset_description = '[{}-{}-{}-{}]'.format(
#        dataset_type, n_datasets, task_size, window_size)
#    #logging.info(dataset_description)
