import Oger
import pylab
import mdp

from rbn_nodes import RBNNode

#[x, y] = Oger.datasets.narma30()

rbn_reservoir = RBNNode(input_connectivity=3, output_dim=5)
#readout = Oger.nodes.RidgeRegressionNode()

training_data = mdp.numx.array([[1], [0], [1], [0], [1], [0]])

print training_data
print rbn_reservoir.execute(training_data)


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
