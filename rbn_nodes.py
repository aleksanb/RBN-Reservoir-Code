import mdp
import numpy


def generate_nodes(n_nodes):
    return numpy.zeros(n_nodes, dtype='int32')


def generate_connections(n_nodes, connectivity):
    return [
        [numpy.random.choice(
            range(n_nodes),
            connectivity,
            replace=False)]
        for n in range(n_nodes)]


def generate_rule(connectivity, expected_p):
    return [numpy.random.binomial(1, expected_p)
            for _ in range(2 ** connectivity)]


def generate_rules(n_nodes, connectivity, expected_p):

    return [generate_rule(connectivity, expected_p) for n in range(n_nodes)]


class RBNNode(mdp.Node):

    def __init__(self, input_dim=None, output_dim=None, dtype='int32',
                 connectivity=2, expected_p=0.5, input_connectivity=None):
        if input_connectivity > output_dim:
            raise mdp.NodeException('Cannot connect more input than available nodes')

        super(RBNNode, self).__init__(
            input_dim=input_dim, output_dim=output_dim, dtype=dtype)

        self.connectivity = connectivity
        self.n_nodes = output_dim
        self.expected_p = expected_p

        if input_connectivity is None:
            input_connectivity = self.n_nodes
        self.input_connections = numpy.random.choice(range(self.n_nodes),
                                                     input_connectivity,
                                                     replace=False)
        self.initialize()

        #print "inpt_conn", self.input_connections
        #print "state", self.nodes
        #print "rules", self.rules
        #print "conns", self.connections

    def _get_supported_dtypes(self):
        return ['int32']

    def is_trainable(self):
        return False

    def is_invertible(self):
        return False

    def initialize(self):
        self.nodes = generate_nodes(self.n_nodes)
        self.connections = generate_connections(self.n_nodes,
                                                self.connectivity)
        self.rules = generate_rules(self.n_nodes,
                                    self.connectivity,
                                    self.expected_p)

    def _execute(self, input_array):
        #print "Executing:", input_array.shape

        output_states = []

        for perturbance in input_array:
            #print "Pre-turb:",self.nodes, "p:", perturbance[0]
            self.perturb_rbn(perturbance[0])
            #print "Pos-turb:", self.nodes
            self.run_crbn()
            output_states.append(self.nodes)
            #print "Post-update", self.nodes

        return output_states

    def perturb_rbn(self, perturbance):
        for node in self.input_connections:
            #self.nodes[node] = self.nodes[node] and perturbance
            #self.nodes[node] = self.nodes[node] ^ perturbance
            self.nodes[node] = perturbance

    def run_crbn(self):
        nodes_next = generate_nodes(self.n_nodes)
        for n in range(self.n_nodes):
            neighbors = self.connections[n]
            neighbor_states = self.nodes[neighbors]
            rule_index = numpy.polyval(neighbor_states, 2)
            new_value = self.rules[n][rule_index]
            nodes_next[n] = new_value

        self.nodes = nodes_next

if __name__ == '__main__':
    rbn_node = RBNNode(input_dim=10, output_dim=10)

    #seen_states = {}
    #for i in range(100):
    #    print str(rbn_node.nodes)
    #    if str(rbn_node.nodes) in seen_states:
    #        print "attractor from", seen_states[str(rbn_node.nodes)], "to", i
    #        break

    #    seen_states[str(rbn_node.nodes)] = i
    #    rbn_node.update()

    #print "Finito!"
