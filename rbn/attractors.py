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
    initial_states = itertools.product([0, 1], repeat=rbn.n_nodes)
    attractors = {}

    transient_times = [find_attractor(rbn, initial_state, attractors)
                       for initial_state in initial_states]

    n_attractors = len(attractors)
    mean_attractor_length = np.mean(map(len, attractors.values()))
    mean_transient_time = np.mean(transient_times)

    return {
        "n_attractors": n_attractors,
        "mean_attractor_length": mean_attractor_length,
        "mean_transient_time": mean_transient_time,
        "attractors": attractors
    }
