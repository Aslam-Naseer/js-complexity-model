import modal

from agents.base_agent import Agent
from llm_model.get_messages import get_messages
from nn_model.artifacts.test_res import test_res
from utils.random_number import biased_random


class LLMAgent(Agent):
    name = "LLM MODEL"
    color = Agent.CYAN

    def __init__(self):
        self.log("LLM Agent is initializing - connecting to modal")
        try:
            ComplexityLLM = modal.Cls.from_name(
                "complexity-service", "ComplexityLLM")
            self.complexity_llm = ComplexityLLM()

            self.log("LLM Agent is ready and connected to modal service")
        except Exception as e:
            self.log(f"Failed to connect to modal service: {e}", is_error=True)

    def predict(self, code: str):
        if not code:
            return None

        self.log("LLM Agent is calling remote fine-tuned model")
        messages = get_messages(code)
        result = self.complexity_llm.complexity.remote(messages)
        self.log(f"LLM Agent completed - predicting Complexity = {result:.2f}")
        return result

    def predict_mock(self, code: str, use_index=False, idx=0):
        if not code:
            return None

        self.log(f"MOCK LLM Agent using predict")
        result = test_res[idx]

        if not use_index:
            result = biased_random(code)

        self.log(
            f"MOCK LLM Agent completed - Randomised Complexity = {result:.2f}")
        return result
