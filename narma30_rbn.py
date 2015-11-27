import Oger
import mdp
import matplotlib.pyplot as plt
import numpy as np

from rbn_nodes import RBNNode

def create_remember_training_data(dataset_length, n_remember):
    input_data = np.random.randint(2, size=dataset_length)
    expected_output = np.empty(dataset_length, dtype='int32')

    for idx in range(dataset_length):
        from_idx = max(idx - n_remember, 0)
        count = sum(input_data[from_idx : idx])
        expected_output[idx] = count % 2 == 1

    return np.transpose([input_data]), np.transpose([expected_output])

input_data, output_data = create_remember_training_data(30, 3)

plt.matshow(input_data, cmap=plt.cm.gray)
plt.title('Input data')
plt.matshow(output_data, cmap=plt.cm.gray)
plt.title('Output data')

#[x, y] = Oger.datasets.narma30()

rbn_reservoir = RBNNode(connectivity=2, input_connectivity=30, output_dim=100, should_perturb=True)
readout = Oger.nodes.RidgeRegressionNode()

#testdata = map(lambda x: [x], numpy.random.randint(2, size=40))
#testdata = numpy.zeros((20, 1), dtype='int32')
#training_data = np.array(testdata)

rbn_states = rbn_reservoir.execute(input_data)

input_connections = np.zeros((1, rbn_reservoir.output_dim), dtype='int32')
input_connections[0, rbn_reservoir.input_connections] = 1

plt.matshow(input_connections, cmap=plt.cm.gray)
plt.title('Input connections')
plt.matshow(rbn_states, cmap=plt.cm.gray)
plt.title('RBN states')
plt.show()




#flow = mdp.Flow([reservoir], verbose=1)
#flow = mdp.Flow([reservoir, readout], verbose=1)
#data = [None, zip(x[0:-1], y[0:-1])]
#data = [x, zip(x, y)]

#flow.train(data)

#expected = y[-1]
#actually = flow(x[-1])

#print "NRMSE: " + str(Oger.utils.nrmse(expected, actually))

#pylab.plot(expected, 'r')
#pylab.plot(actually, 'b')
#pylab.show()
