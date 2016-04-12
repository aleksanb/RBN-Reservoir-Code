from sklearn.linear_model import Ridge

class ReservoirSystem():

    def __init__(self, rbn_reservoir):
        self.rbn_reservoir = rbn_reservoir
        self.readout_layer = Ridge()

    def train_on(self, training_input, training_output):
        training_states = self.rbn_reservoir.execute(training_input)
        self.readout_layer.fit(training_states, training_output)

    def test_on(self, test_input, test_output):
        test_states = self.rbn_reservoir.execute(test_input)
        predictions = self.readout_layer.predict(test_states)

        for prediction in predictions:
            prediction[0] = 1 if prediction[0] > 0.5 else 0

        errors = sum(predictions != test_output)
        accuracy = 1 - float(errors) / len(predictions)

        return accuracy
