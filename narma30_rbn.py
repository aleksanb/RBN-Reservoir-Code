import Oger
import mdp
import matplotlib.pyplot as plt
import numpy as np

from rbn_nodes import RBNNode
from tasks import temporal

training_dataset, test_dataset = temporal.create_datasets(5,
        task_size=150,
        delay=0,
        window_size=3,
        dataset_type="temporal_parity")

#plt.matshow(test_dataset[0], cmap=plt.cm.gray)
#plt.title('Test input')
#plt.matshow(test_dataset[1], cmap=plt.cm.gray)
#plt.title('Test output')

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
