from tasks.temporal import create_datasets
from rbn.sklearn_rbn_node import RBNNode
from sklearn.linear_model import Ridge

datasets = create_datasets(
    10,
    task_size=200,
    window_size=3,
    dataset_type='temporal_parity')

training_datasets, test_dataset = datasets[:-1], datasets[-1]
rbn_reservoir = RBNNode(connectivity=3,
                        input_connectivity=50,
                        n_nodes=100,
                        output_connectivity=0)
readout_layer = Ridge()

for td in training_datasets[:1]:
    rbn_reservoir.reset_state()

    reservoir_input, expected_output = td

    states = rbn_reservoir.execute(reservoir_input)
    readout_layer.fit(states, expected_output)
    predictions = readout_layer.predict(states)

    for prediction in predictions:
        prediction[0] = 1 if prediction[0] > 0.5 else 0

    errors = sum(predictions != expected_output)
    accuracy = 1 - float(errors) / len(predictions)

    print("Accuracy: {} on {} items."
                 .format(accuracy, len(predictions)))
