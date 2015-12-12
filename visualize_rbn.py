from tasks import temporal
import matplotlib.pyplot as plt
from utils import *
import json

def plot_fitness():
    with open('state.dat', 'r') as states:
        plots = []
        for line in states.readlines():
            state = json.loads(line)
            print state['generation']
            #print line
            #            'children': map(lambda x: x.serialize(), children),
            #            'adults': map(lambda x: x.serialize(), adults),
            #            'generation': generation,
            #            'time': arrow.utcnow().isoformat(),


if __name__ == '__main__':
    plot_fitness()
    import sys
    sys.exit()

    # Create datasets
    dataset_type = default_input('Dataset [temporal_parity, temporal_density]',
                                 'temporal_parity')
    n_datasets = default_input('Datasets', 10)
    task_size = default_input('Dataset length', 200)
    window_size = default_input('Window size', 3)

    datasets = temporal.create_datasets(
        n_datasets,
        task_size=task_size,
        window_size=window_size,
        dataset_type=dataset_type)
    training_dataset, test_dataset = datasets[:-1], datasets[-1]

    dataset_description = '[{}-{}-{}-{}]'.format(
        dataset_type, n_datasets, task_size, window_size)
    #logging.info(dataset_description)

    plt.matshow(test_dataset[0][:20], cmap=plt.cm.gray)
    plt.title('Test input')
    plt.matshow(test_dataset[1][:20], cmap=plt.cm.gray)
    plt.title('Test output')
    plt.show()
