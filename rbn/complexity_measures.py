import numpy as np


def measure_perturbance_spread(reservoir, input_1, input_2):
    if len(input_1) != len(input_2):
        raise ValueError("Cannot measure perturbance spread." +
                         "Received two different-length inputs.")

    reservoir.reset_state()
    end_state_1 = reservoir.execute(input_1)[-1]

    reservoir.reset_state()
    end_state_2 = reservoir.execute(input_2)[-1]

    hamming_distance = float(sum(end_state_1 != end_state_2))

    return hamming_distance / len(end_state_1)


def measure_separation(reservoir, input_size, n_separated_ago):
    if n_separated_ago > input_size:
        raise ValueError("Separation point has to be lower than size of input")

    input_1 = np.random.randint(2, size=(input_size, 1))
    input_2 = np.copy(input_1)
    separation_idx = input_size - 1 - n_separated_ago
    input_2[separation_idx:] = 1 - input_2[separation_idx:]

    return measure_perturbance_spread(reservoir, input_1, input_2)


def measure_fading_memory(reservoir, input_size):
    input_1 = np.random.randint(2, size=(input_size, 1))
    input_2 = np.copy(input_1)
    input_2[0] = 1 - input_2[0]

    return measure_perturbance_spread(reservoir, input_1, input_2)


def measure_computational_capability(reservoir, input_size, n_separated_ago):
    separation = measure_separation(reservoir, input_size, n_separated_ago)
    fading = measure_fading_memory(reservoir, input_size)

    return separation - fading
