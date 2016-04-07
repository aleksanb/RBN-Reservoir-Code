import numpy as np
import itertools


def find_attractor(rbn, initial_state, attractors):
    rbn.state = np.array(initial_state)
    current_state = np.polyval(rbn.state, 2)

    visited_states = []
    in_existing_attractor = False

    while True:
        visited_states.append(current_state)
        rbn._run_crbn()
        current_state = np.polyval(rbn.state, 2)

        if current_state in attractors:
            # No break as we want to go the full loop
            in_existing_attractor = current_state

        if current_state in visited_states:
            if in_existing_attractor:
                transient_time = len(visited_states) - len(attractors[in_existing_attractor])
                return transient_time

            # We're the first to find this attractor!
            attractor_begin = visited_states.index(current_state)
            attractor_length = len(visited_states) - attractor_begin
            attractors[current_state] = visited_states[attractor_begin:]

            return attractor_begin


def find_attractors(rbn, print_progress=True):
    four = 2 ** reservoir_size / 25
    progress = 0

    initial_states = itertools.product([0, 1], repeat=rbn.n_nodes)
    attractors = {}
    transient_times = []

    for idx, initial_state in enumerate(initial_states):
        transient_time  = find_attractor(rbn, initial_state, attractors)
        transient_times.append(transient_time)

        if print_progress and (idx % four == 0):
            print "{}%".format(progress)
            progress += 4

    return attractors, transient_times


from rbn.sklearn_rbn_node import RBNNode
reservoir_size = 10

rbn = RBNNode(connectivity=3,
              input_connectivity=reservoir_size/2,
              n_nodes=reservoir_size,
              should_perturb=False)

a, t = find_attractors(rbn)

print "Attractors:", a
print "Transients", t
