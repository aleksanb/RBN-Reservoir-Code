import Oger
import mdp
#import matplotlib.pyplot as plt
import math
import numpy as np

from utils import confirm, default_input, dump, load
from rbn import rbn_node
from tasks import temporal

from rbn_reservoir_problem import RBNReservoirProblem
from ea.solve import solve

import log
import logging

log.setup(logging.DEBUG)


def rbn_genome_size(n_nodes, connectivity):
    bits_for_input_connection = 1
    bits_for_node_neighbors = connectivity * int(
        math.ceil(math.log(n_nodes, 2)))
    bits_for_transition_table = connectivity

    bits_per_node = (bits_for_input_connection +
                     bits_for_node_neighbors +
                     bits_for_transition_table)

    return bits_per_node * n_nodes


#plt.matshow(test_dataset[0][:10], cmap=plt.cm.gray)
#plt.title('Test input')
#plt.matshow(test_dataset[1][:10], cmap=plt.cm.gray)
#plt.title('Test output')


if __name__ == '__main__':
    # Create datasets
    dataset_type = "temporal_parity"
    datasets = default_input('Datasets', 10)
    task_size = default_input('Dataset length', 200)
    window_size = default_input('Window size', 3)

    problem_description = '[{}-{}-{}-{}]'.format(
        dataset_type, datasets, task_size, window_size)
    logging.info(problem_description)

    datasets = temporal.create_datasets(
        datasets,
        task_size=task_size,
        window_size=window_size,
        dataset_type=dataset_type)
    training_dataset, test_dataset = datasets[:-1], datasets[-1]

    # Create or load reservoir and readout layer
    if confirm('Use existing readout layer?'):
        readout = load('Readout pickle:', folder='working_flows')
    else:
        connectivity = default_input('connectivity', 2)
        n_nodes = default_input('n_nodes', 100)
        input_connectivity = default_input('input_connectivity', 50)
        rbn_reservoir = rbn_node.RBNNode(connectivity=connectivity,
                                         output_dim=n_nodes,
                                         input_connectivity=input_connectivity)

        readout = Oger.nodes.RidgeRegressionNode(input_dim=n_nodes,
                                                 output_dim=1,
                                                 verbose=True)

        # Train and execute newly created flow
        flow = mdp.Flow([rbn_reservoir, readout], verbose=1)
        flow.train([None, training_dataset])

        reservoir_input, expected_output = test_dataset
        actual_output = flow.execute(reservoir_input)
        for output in actual_output:
            output[0] = 1 if output[0] > 0.5 else 0

        errors = sum(actual_output != expected_output)
        accuracy = 1 - float(errors) / len(actual_output)
        logging.info("Accuracy: {} ({} error(s) out of {})"
                     .format(accuracy, errors[0], len(actual_output)))

        # Optionally dump newly created flow
        if confirm('Pickle reservoir and readout layer?'):
            flow_description = '{}-{}-[ACC:{}]'.format(
                problem_description,
                rbn_reservoir.describe(),
                accuracy)
            dump(rbn_reservoir, flow_description + '-reservoir',
                 folder='working_flows')
            dump(readout, flow_description + '-readout',
                 folder='working_flows')

    # Evolve other reservoirs with similar dynamics
    if confirm('Use readout layer to evolve similar rbn_reservoirs?'):
        connectivity = default_input('Connectivity', 2)
        n_nodes = readout.input_dim

        reservoir_problem = RBNReservoirProblem(
            n_nodes, connectivity, readout, test_dataset)

        generation, adults = solve(reservoir_problem)

        fitnesses = [x.fitness for x in adults]
        top3 = fitnesses[-3:]
        top3.reverse()
        mean = np.mean(fitnesses)
        std = np.std(fitnesses)

        description = '{}-[N:{}-K:{}]-[TOP:{}-MEAN:{}-STD:{}-GEN:{}]'.format(
            problem_description,
            n_nodes,
            connectivity,
            '{}'.format(top3),
            fitnesses[-1],
            mean,
            std,
            generation)
        dump(adults, description, folder='evolved_rbns')

        logging.info('GA run completed, adults pickled')

#plt.plot(actual_output, 'r')
#plt.plot(expected_output, 'b')
#plt.show()

#plt.matshow(input_connections, cmap=plt.cm.gray)
#plt.title('Input connections')
#plt.matshow(rbn_states, cmap=plt.cm.gray)
#plt.title('RBN states')
#plt.show()
