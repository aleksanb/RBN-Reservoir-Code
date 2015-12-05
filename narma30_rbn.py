import Oger
import mdp
import matplotlib.pyplot as plt
import numpy as np

from rbn_nodes import RBNNode


def create_dataset(dataset_length, n_remember):
    input_data = np.random.randint(2, size=dataset_length)
    expected_output = np.zeros(dataset_length, dtype='int')

    for idx in range(dataset_length):
        from_idx = max(idx - n_remember, 0)
        count = sum(input_data[from_idx:idx])
        expected_output[idx] = count % 2 == 1

    return (np.transpose([input_data]), np.transpose([expected_output]))


training_dataset = [create_dataset(1000, 2) for _ in range(10)]
test_dataset = create_dataset(1000, 2)

n_nodes = 100
rbn_reservoir = RBNNode(connectivity=2,
                        input_connectivity=n_nodes/2,
                        output_dim=n_nodes,
                        should_perturb=True)
readout = Oger.nodes.RidgeRegressionNode(input_dim=n_nodes,
                                         output_dim=1,
                                         verbose=True)

flow = mdp.Flow([rbn_reservoir, readout], verbose=1)
flow.train([None, training_dataset])

reservoir_input = test_dataset[0]
expected_output = test_dataset[1]

actual_output = flow.execute(reservoir_input)
avg = 0.5#np.average(actual_output)
for i in range(actual_output.shape[0]):
    actual_output[i][0] = 1 if actual_output[i][0] > avg else 0


errors = sum(actual_output != expected_output)
print "Errors: ", errors, " of ", len(actual_output)

plt.plot(actual_output, 'r')
plt.plot(expected_output, 'b')
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

#print "NRMSE: " + str(Oger.utils.nrmse(expected, actually))

#pylab.plot(expected, 'r')
#pylab.plot(actually, 'b')
#pylab.show()
