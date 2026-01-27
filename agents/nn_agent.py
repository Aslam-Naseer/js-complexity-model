import joblib
import torch

from agents.base_agent import Agent
from nn_model.normalise_features import normalise_features
from nn_model.complexity_nn import NeuralNetwork

feature_cols = [
    'parameterCount',
    'statementCount',
    'variableCount',
    'maxNestingDepth'
]


class NNAgent(Agent):
    name = "NEURAL NET"
    color = Agent.YELLOW

    def __init__(self):
        self.log("Neural Network Agent is initializing")

        self.scaler = joblib.load('nn_model/artifacts/scaler.pkl')
        self.model = NeuralNetwork(input_size=len(feature_cols))
        self.model.load_state_dict(torch.load(
            'nn_model/artifacts/neural_network.pth'))
        self.model.eval()

        self.log("Neural Network Agent is ready and weights are loaded")

    def predict(self, features: dict):
        if not features:
            return None

        if not all(col in features for col in feature_cols):
            self.log("Missing required features for NN prediction", is_error=True)
            return None

        self.log("Neural Network Agent is starting a prediction")
        self.log(f"Input features: {features}")

        features = normalise_features(features, self.scaler)['features']
        features_tensor = torch.tensor(features, dtype=torch.float32)
        with torch.no_grad():
            prediction = self.model(features_tensor)
            self.log(
                f"Neural Network Agent completed - predicting Complexity = {prediction[0].item():.2f}")

        return prediction[0].item()
