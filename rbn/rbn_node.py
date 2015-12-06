import mdp
import numpy


def create_empty_state(n_nodes):
    return numpy.zeros(n_nodes, dtype='int')


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

    def __init__(self, input_dim=None, output_dim=None, dtype='int',
                 connectivity=2, expected_p=0.5, input_connectivity=None,
                 n_runs_after_perturb=1, should_perturb=True,
                 heterogenous=False):
        if input_connectivity > output_dim:
            raise mdp.NodeException(
                'Cannot connect more input than available nodes')

        super(RBNNode, self).__init__(
            input_dim=input_dim, output_dim=output_dim, dtype=dtype)

        self.connectivity = connectivity
        self.n_nodes = output_dim
        self.expected_p = expected_p
        self.n_runs_after_perturb = n_runs_after_perturb
        self.should_perturb = should_perturb

        if input_connectivity is None:
            input_connectivity = self.n_nodes
        self.input_connections = numpy.random.choice(range(self.n_nodes),
                                                     input_connectivity,
                                                     replace=False)
        self.initialize()

    def _get_supported_dtypes(self):
        return ['int']

    def is_trainable(self):
        return False

    def is_invertible(self):
        return False

    def initialize(self):
        self.state = create_empty_state(self.n_nodes)
        self.connections = generate_connections(self.n_nodes,
                                                self.connectivity)
        self.rules = generate_rules(self.n_nodes,
                                    self.connectivity,
                                    self.expected_p)

    def _execute(self, input_array):
        steps = input_array.shape[0]

        output_states = numpy.zeros((steps, self.output_dim))

        for step in range(steps):
            perturbance = input_array[step][0]
            if self.should_perturb:
                self.perturb_rbn(perturbance)
            for _ in range(self.n_runs_after_perturb):
                self.run_crbn()
            output_states[step] = self.state

        return output_states

    def perturb_rbn(self, perturbance):
        self.state[self.input_connections] = perturbance

    def run_crbn(self):
        next_state = create_empty_state(self.n_nodes)
        for n in range(self.n_nodes):
            neighbors = self.connections[n]
            neighbor_states = self.state[neighbors]
            rule_index = numpy.polyval(neighbor_states, 2)
            new_value = self.rules[n][rule_index]
            next_state[n] = new_value

        self.state = next_state

    def reset_state(self):
        self.state = create_empty_state(self.n_nodes)
