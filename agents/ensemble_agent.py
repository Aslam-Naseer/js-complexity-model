from agents.base_agent import Agent
from agents.llm_agent import LLM_Agent
from agents.nn_agent import NN_Agent

NN_BIAS = 0.3
LLM_BIAS = 0.7

feature_cols = ['parameter_count', 'statement_count',
                'variable_count', 'max_nesting_depth']


class Ensemble_Agent(Agent):
    name = "Ensemble Agent"
    color = Agent.YELLOW

    def __init__(self):
        self.log("Initializing Ensemble Agent...")
        self.llm_agent = LLM_Agent()
        self.nn_agent = NN_Agent()
        self.log("Ensemble Agent ready.")

    def predict(self, data):
        has_nn_data = all(col in data for col in feature_cols)
        has_llm_data = 'code' in data and data['code']

        nn_score = None
        llm_score = None

        if has_nn_data:
            nn_score = self.nn_agent.predict(data)
        else:
            self.log("Skipping NN: Missing feature columns.")

        if has_llm_data:
            llm_score = self.llm_agent.predict(data['code'])
        else:
            self.log("Skipping LLM: Missing 'code' field.")

        if nn_score is not None and llm_score is not None:
            final_score = (NN_BIAS * nn_score) + (LLM_BIAS * llm_score)

        elif nn_score is not None:
            final_score = nn_score

        elif llm_score is not None:
            final_score = llm_score

        else:
            self.log("Error: Insufficient data for prediction.")
            return 0.0

        self.log(
            f"Ensemble Agent completed - predicting Complexity = {final_score:.2f}")
        return round(final_score, 1)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)

    print("--- STARTING TEST ---")

    # 1. Define Test Dataset (using JavaScript codes)
    test_dataset = [
        {
            "id": 1,
            "description": "CASE 1: Full Data (Complex JS)",
            "code": """
                function calculatePrimes(n) {
                    const primes = [];
                    for (let i = 2; i < n; i++) {
                        let isPrime = true;
                        for (let j = 2; j <= Math.sqrt(i); j++) {
                            if (i % j === 0) isPrime = false;
                        }
                        if (isPrime) primes.push(i);
                    }
                    return primes;
                }
            """,
            "parameter_count": 1,
            "statement_count": 8,
            "variable_count": 3,
            "max_nesting_depth": 3
        },
        {
            "id": 2,
            "description": "CASE 2: NN Data Only (Missing Code)",
            # "code" is missing intentionally
            "parameter_count": 0,
            "statement_count": 1,
            "variable_count": 0,
            "max_nesting_depth": 0
        },
        {
            "id": 3,
            "description": "CASE 3: LLM Data Only (Missing Features)",
            "code": "const add = (a, b) => a + b;",
            # Feature columns are missing intentionally
        }
    ]

    # 2. Initialize Agent
    agent = Ensemble_Agent()
    print("-" * 30)

    # 3. Run Tests
    for data in test_dataset:
        print(f"\nTesting: {data['description']}")

        try:
            score = agent.predict(data)
            print(f"Result -> Score: {score}")
        except Exception as e:
            logging.error(f"Test Failed: {e}")

    print("\n--- TEST COMPLETE ---")
