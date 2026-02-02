from typing import Optional
from agents.base_agent import Agent
from agents.llm_agent import LLMAgent
from agents.nn_agent import NNAgent


class Evaluator(Agent):
    name = "EVALUATOR"
    color = Agent.MAGENTA

    def __init__(self, nn_bias=0.3, llm_bias=0.7):
        super().__init__()
        self.log("Initializing Evaluation Agent...")
        self.llm_agent = LLMAgent()
        self.nn_agent = NNAgent()

        self.nn_bias = nn_bias
        self.llm_bias = llm_bias
        self.log("Evaluator is ready.")

    def predict(self, code_str: Optional[str] = None, features: Optional[dict] = None):
        """
        Unified predict method. 
        Accepts code and/or features explicitly.
        """
        nn_score = None
        llm_score = None

        if code_str:
            try:
                llm_score = self.llm_agent.predict(code_str)
            except Exception as e:
                self.log(f"LLM Agent failed: {e}", is_error=True)
        else:
            self.log("Skipping LLM: No code string provided.")

        if features:
            try:
                nn_score = self.nn_agent.predict(features)
            except Exception as e:
                self.log(f"NN Agent failed: {e}", is_error=True)
        else:
            self.log("Skipping NN: No feature dictionary provided.")

        return self._calculate_weighted_score(llm_score, nn_score)

    def _calculate_weighted_score(self, llm_score, nn_score):
        """Helper to keep the math clean and separate."""

        if nn_score is not None and llm_score is not None:
            final = (self.nn_bias * nn_score) + (self.llm_bias * llm_score)
            self.log(f"Combined Score: {final:.2f}")
            return round(final, 2)

        elif nn_score is not None:
            self.log(f"Using NN Score only: {nn_score}")
            return round(nn_score, 2)

        elif llm_score is not None:
            self.log(f"Using LLM Score only: {llm_score}")
            return round(llm_score, 2)

        else:
            return 0.0
