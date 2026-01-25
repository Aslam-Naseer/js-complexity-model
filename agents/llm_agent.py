import modal

from agents.base_agent import Agent
from llm_model.get_messages import get_messages
from nn_model.artifacts.test_res import test_res


class LLM_Agent(Agent):
    name = "LLM Agent"
    color = Agent.CYAN

    def __init__(self):
        self.log("LLM Agent is initializing - connecting to modal")
        ComplexityLLM = modal.Cls.from_name(
            "complexity-service", "ComplexityLLM")
        self.complexity_llm = ComplexityLLM()

    def predict(self, code) -> float:
        self.log("LLM Agent is calling remote fine-tuned model")
        messages = get_messages(code)
        result = self.complexity_llm.complexity.remote(messages)
        self.log(f"LLM Agent completed - predicting Complexity = {result:.2f}")
        return result

    def predict_saved(self, idx):
        return test_res[idx]
