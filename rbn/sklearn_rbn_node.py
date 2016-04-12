import numpy


class RBNNode():
    def __init__(self,
                 n_nodes=100, connectivity=2, expected_p=0.5,
                 input_connectivity=None, input_connections=None,
                 n_runs_after_perturb=1, should_perturb=True,
                 connections=None,
                 rules=None,
                 output_connectivity=None):
        self.n_nodes = n_nodes
        self.connectivity = connectivity
        self.expected_p = expected_p

        self.n_runs_after_perturb = n_runs_after_perturb
        self.should_perturb = should_perturb

        # Initialize unique numpy random for use with multiprocessing
        self.npr = numpy.random.RandomState()

        # Initialize state and connections

        self.state = self._empty_state()

        if input_connections is not None:
            self.input_connectivity = len(input_connections)
            self.input_connections = input_connections
        elif input_connectivity is not None:
            self.input_connectivity = input_connectivity
            self.input_connections =\
                self.npr.choice(self.n_nodes,
                                self.input_connectivity,
                                replace=False)
        else:
            raise Exception('Must provide either input_connections or input_connectivity')

        if connections is not None:
            self.connections = connections
        else:
            self.connections = numpy.array([self.npr.choice(
                    self.n_nodes,
                    self.connectivity,
                    replace=False)
                    for _ in range(self.n_nodes)])

        if rules is not None:
            self.rules = rules
        else:
            self.rules = self.npr.binomial(
                    1,
                    self.expected_p,
                    size=(self.n_nodes, 2 ** self.connectivity))

        if output_connectivity is None:
            output_connectivity = self.n_nodes

        self.output_connectivity = output_connectivity

    def _empty_state(self):
        return numpy.zeros(self.n_nodes, dtype='int')

    def execute(self, input_array):
        steps = input_array.shape[0]

        output_states = numpy.zeros((steps, self.output_connectivity))

        for step in range(steps):
            perturbance = input_array[step][0]

            if self.should_perturb:
                self.state[self.input_connections] = perturbance

            for _ in range(self.n_runs_after_perturb):
                self._run_crbn()

            output_states[step] = self.state[:self.output_connectivity]

        return output_states

    def _run_crbn(self):
        next_state = self._empty_state()

        for n in range(self.n_nodes):
            neighbors = self.connections[n]
            neighbor_states = self.state[neighbors]
            rule_index = numpy.polyval(neighbor_states, 2)
            new_value = self.rules[n][rule_index]
            next_state[n] = new_value

        self.state = next_state

    def __repr__(self):
        return "[N:{}-K:{}-I:{}-O:{}]".format(
            self.n_nodes, self.connectivity, self.input_connectivity, self.output_connectivity)
