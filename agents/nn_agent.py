import modal
from agents.base_agent import Agent


class NNAgent(Agent):
    name = "NN MODEL"
    color = Agent.CYAN

    def __init__(self):
        self.log("NN Agent is initializing - connecting to modal")
        try:
            ComplexityNN = modal.Cls.from_name(
                "nn-service", "ComplexityNN")
            self.complexity_nn = ComplexityNN()

            self.log("NN Agent is ready and connected to modal service")
        except Exception as e:
            self.log(f"Failed to connect to modal service: {e}", is_error=True)

    def predict(self, features: dict):
        if not features:
            return None

        self.log(f"NN Agent is calling remote model")
        result = self.complexity_nn.predict.remote(features)
        self.log(f"NN Agent completed - predicting Complexity = {result:.2f}")
        return result
