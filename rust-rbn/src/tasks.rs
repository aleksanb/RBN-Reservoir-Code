use utils;

#[derive(Debug)]
pub struct Task {
    pub input: Vec<u8>,
    pub output: Vec<u8>,
}

pub enum TaskType {
    TemporalParity,
    TemporalDensiy,
}

impl Task {
    pub fn new(task_type: TaskType,
                       task_size: usize,
                       window_size: usize) -> Self {
        let input = utils::rand_bits(task_size);
        let mut output = vec![0; task_size];

        for i in (window_size-1)..input.len() {
            let to_idx = i + 1;
            let from_idx = to_idx - window_size;

            let out = input[from_idx..to_idx].iter().sum::<u8>();
            output[i] = out % 2;
        }

        Task {
            input: input,
            output: output,
        }
    }
}
/*
fn temporal_parity()

def temporal_parity

import numpy as np


def generic_temporal(label_function, task_size, delay, window_size):
    input_data = np.random.randint(2, size=task_size)
    labels = np.zeros(task_size, dtype='int')

    for i in range(task_size):
    to_idx = i + 1 - delay
    from_idx = max(to_idx - window_size, 0)

    labels[i] = label_function(input_data[from_idx:to_idx], window_size)

return np.transpose([input_data]), np.transpose([labels])


    def temporal_parity(array, window_size):
        return sum(array) % 2 == 1


        def temporal_density(array, window_size):
            if window_size % 2 == 0:
            raise ValueError("Temporal density requires window size to be odd")

            return 2 * sum(array) > len(array)


    def create_datasets(n_datasets,
                        task_size=1000,
                        delay=0,
                        window_size=2,
                        dataset_type=None):

        label_function = { 
            'temporal_parity': temporal_parity,
            'temporal_density': temporal_density
        }[dataset_type]

return [generic_temporal(label_function,
                         task_size,
                         delay,
                         window_size)
    for _ in range(n_datasets)]
    ~                                           */
