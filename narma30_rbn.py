import Oger
import mdp
import matplotlib.pyplot as plt
import pickle
import time

from rbn import rbn_node, complexity_measures
from tasks import temporal

def dump_reservoir(reservoir):
    complexity = complexity_measures.measure_computational_capability(rbn_reservoir, 10, 0)
    path = "pickle_dumps/{}-[{}].pickle".format(time.time(), complexity)
    pickle.dump(rbn_reservoir, open(path, 'w'))

def get_reservoir(path):
    return pickle.load(open(path, 'r'))

gotta_remember = 5

training_dataset, test_dataset = temporal.create_datasets(
    5,
    task_size=150,
    delay=0,
    window_size=gotta_remember,
    dataset_type="temporal_density")

plt.matshow(test_dataset[0][:10], cmap=plt.cm.gray)
plt.title('Test input')
plt.matshow(test_dataset[1][:10], cmap=plt.cm.gray)
plt.title('Test output')

n_nodes = 200
rbn_reservoir = rbn_node.RBNNode(connectivity=2,
                                 heterogenous=True,
                                 input_connectivity=70,
                                 output_dim=n_nodes,
                                 should_perturb=True)
#rbn_reservoir = get_reservoir("pickle_dumps/[1449435450.66]-[0.213333333333].pickle")

#dump_reservoir(rbn_reservoir)

print complexity_measures.measure_computational_capability(rbn_reservoir, 100, gotta_remember)

readout = Oger.nodes.RidgeRegressionNode(input_dim=n_nodes,
                                         output_dim=1,
                                         verbose=True)

flow = mdp.Flow([rbn_reservoir, readout], verbose=1)
flow.train([None, training_dataset])

reservoir_input = test_dataset[0]
expected_output = test_dataset[1]

actual_output = flow.execute(reservoir_input)
for i in range(actual_output.shape[0]):
    actual_output[i][0] = 1 if actual_output[i][0] > 0.5 else 0


errors = sum(actual_output != expected_output)
print "Errors: ", errors, " of ", len(actual_output)

#plt.plot(actual_output, 'r')
#plt.plot(expected_output, 'b')
plt.show()


#rbn_states = rbn_reservoir.execute(input_data)


#input_connections = np.zeros((1, rbn_reservoir.output_dim), dtype='int32')
#input_connections[0, rbn_reservoir.input_connections] = 1
##
#plt.matshow(input_connections, cmap=plt.cm.gray)
#plt.title('Input connections')
#plt.matshow(rbn_states, cmap=plt.cm.gray)
#plt.title('RBN states')
#plt.show()
