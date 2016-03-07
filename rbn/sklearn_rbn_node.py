import numpy

def create_empty_state(n_nodes):
    return numpy.zeros(n_nodes, dtype='int')


def generate_connections(n_nodes, connectivity):
    return [
        numpy.random.choice(
            range(n_nodes),
            connectivity,
            replace=False)
        for n in range(n_nodes)]


def generate_rule(connectivity, expected_p):
    return [numpy.random.binomial(1, expected_p)
            for _ in range(2 ** connectivity)]


def generate_rules(n_nodes, connectivity, expected_p):
    return [generate_rule(connectivity, expected_p) for n in range(n_nodes)]


class RBNNode():
    def __init__(self,
                 n_nodes=100, connectivity=2, expected_p=0.5,
                 input_connectivity=None, input_connections=None,
                 n_runs_after_perturb=1, should_perturb=True,
                 connections=None,
                 rules=None):
        self.n_nodes = n_nodes
        self.connectivity = connectivity
        self.expected_p = expected_p

        self.n_runs_after_perturb = n_runs_after_perturb
        self.should_perturb = should_perturb

        # Initialize state and connections
        self.reset_state()

        if input_connections is not None:
            self.input_connectivity = len(input_connections)
            self.input_connections = input_connections
        elif input_connectivity is not None:
            self.input_connectivity = input_connectivity
            self.input_connections =\
                numpy.random.choice(range(self.n_nodes),
                                    self.input_connectivity,
                                    replace=False)
        else:
            raise Exception('Must provide either input_connections or input_connectivity')

        if connections is not None:
            self.connections = connections
        else:
            self.connections = generate_connections(self.n_nodes,
                                                    self.connectivity)
        if rules is not None:
            self.rules = rules
        else:
            self.rules = generate_rules(self.n_nodes,
                                        self.connectivity,
                                        self.expected_p)

    def execute(self, input_array):
        steps = input_array.shape[0]

        output_states = numpy.zeros((steps, self.n_nodes))

        for step in range(steps):
            perturbance = input_array[step][0]
            if self.should_perturb:
                self._perturb_rbn(perturbance)
            for _ in range(self.n_runs_after_perturb):
                self._run_crbn()
            output_states[step] = self.state

        return output_states

    def _perturb_rbn(self, perturbance):
        self.state[self.input_connections] = perturbance

    def _run_crbn(self):
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

    def __repr__(self):
        return "[N:{}-K:{}-I:{}]".format(
            self.n_nodes, self.connectivity, self.input_connectivity)
