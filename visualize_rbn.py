import matplotlib.pyplot as plt

import networkx as nx
from utils import get_working_dir, glob_load, user_denies, user_confirms
import numpy as np
import json

from itertools import repeat
import mdp

import log
import logging

import re


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


def visualize_dataset(n=30, working_dir=None):
    if not working_dir:
        working_dir = get_working_dir()

    test_dataset, filename = glob_load(working_dir + '*-dataset')[0]

    dataset_meta = re.search(r"\[(.*)\]", filename).groups()[0]

    reservoir_input = np.transpose(test_dataset[0][:n])
    expected_output = np.transpose(test_dataset[1][:n])

    plt.matshow(reservoir_input, cmap=plt.cm.gray)
    plt.axis('off')
    plt.savefig('plots/' + dataset_meta + '-input.pdf', bbox_inches='tight')

    plt.matshow(expected_output, cmap=plt.cm.gray)
    plt.axis('off')
    plt.savefig('plots/' + dataset_meta + '-output.pdf', bbox_inches='tight')

    plt.show()


def visualize_correctness(n=25, working_dir=None):
    if not working_dir:
        working_dir = get_working_dir()

    (reservoir_input, expected_output), _ =\
        glob_load(working_dir + '*-dataset')[0]
    rbn_reservoir, _ = glob_load(working_dir + '*-reservoir')[0]
    readout, _ = glob_load(working_dir + '*-readout')[0]

    rbn_reservoir.reset_state()
    flow = mdp.Flow([rbn_reservoir, readout], verbose=1)

    actual_output = flow.execute(reservoir_input)
    for output in actual_output:
        output[0] = 1 if output[0] > 0.5 else 0

    errors = sum(actual_output != expected_output)
    accuracy = 1 - float(errors) / len(actual_output)

    plt.title('Reservoir performance')
    plt.plot(actual_output[:n], 'y', linewidth=1.5)
    plt.plot(expected_output[:n], 'b', linewidth=1.5)
    plt.legend(['Actual output', 'Expected output'])

    plt.savefig('temp-2.pdf', bbox_inches='tight')


#def plot_fitness():
#    with open('state.dat', 'r') as states:
#        plots = []
#        for line in states.readlines():
#            state = json.loads(line)
#            print state['generation']
#            #print line
#            #            'children': map(lambda x: x.serialize(), children),
#            #            'adults': map(lambda x: x.serialize(), adults),
#            #            'generation': generation,
#            #            'time': arrow.utcnow().isoformat(),


#visualize_dataset()

def visualize_rbn_state(n=100, working_dir=None):
    if not working_dir:
        working_dir = get_working_dir()

    rbn, rbn_name = glob_load(working_dir + '*-reservoir')[0]
    rbn.reset_state()

    if not user_denies('Perturb?'):
        test_data, _ = glob_load(working_dir + '*-dataset')[0]
        test_input, _ = test_data
        test_input = test_input[:n]
    else:
        test_input = np.zeros((n, 1))
        rbn.should_perturb = False

    rbn_states = rbn._execute(test_input)

    plt.matshow(rbn_states, cmap=plt.cm.gray)
    plt.xlabel('State of node n in RBN')
    plt.gca().xaxis.set_label_position('top')
    plt.ylabel('Time')

    plt.savefig(raw_input('Name: '), bbox_inches='tight')
    plt.show()

    #plt.matshow(test_input, cmap=plt.cm.gray)
    #plt.title('Reservoir input')

    #input_connections = np.zeros((1, rbn.n_nodes))
    #input_connections[0, rbn.input_connections] = 1

    #plt.matshow(input_connections, cmap=plt.cm.gray)
    #plt.title('Input connections')

    #plt.show()

if __name__ == '__main__':
    log.setup(logging.DEBUG)

    visualize_dataset()

    import sys
    sys.exit()

    from rbn import rbn_node

    rbn_reservoir_ordered = rbn_node.RBNNode(
            connectivity=2,
            should_perturb=False,
            output_dim=30,
            input_connectivity=15)
    #rbn_reservoir_critical = rbn_node.RBNNode(
    #        connectivity=2,
    #        should_perturb=False,
    #        output_dim=30,
    #        input_connectivity=15)
    #rbn_reservoir_chaotic = rbn_node.RBNNode(
    #        connectivity=4,
    #        should_perturb=False,
    #        output_dim=30,
    #        input_connectivity=15)


    test_input = np.zeros((60, 1))
    ordered = rbn_reservoir_ordered._execute(test_input)
    #critical= rbn_reservoir_critical._execute(test_input)
    #chaotic = rbn_reservoir_chaotic._execute(test_input)

    plt.matshow(ordered, cmap=plt.cm.gray)
    plt.axis('off')
    plt.savefig('plots/critical-phase-new.pdf', bbox_inches='tight')

    #plt.matshow(critical, cmap=plt.cm.gray)
    #plt.axis('off')
    #plt.savefig('plots/critical-phase.pdf', bbox_inches='tight')

    #plt.matshow(chaotic, cmap=plt.cm.gray)
    #plt.axis('off')
    #plt.savefig('plots/chaotic-phase.pdf', bbox_inches='tight')


    #if user_confirms('Visualize rbn state?'):
    #visualize_rbn_state()

    #if user_confirms('Visualize dataset?'):
    #    visualize_dataset()

    #visualize_correctness()


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
