from agents.base_agent import Agent
from agents.evaluator import Evaluator
from utils.code_parser import flatten_functions
from code_analyzer import analyze


class ComplexityOrchestrator(Agent):
    name = "ORCHESTRATOR"
    color = Agent.GREEN

    def __init__(self):
        super().__init__()  # Ensure base Agent init is called
        self.log("Initializing dependencies...")
        self.agent = Evaluator()
        self.log("Complexity Orchestrator is ready.")
        self.log("")

    def process_file(self, full_code_string):
        self.log("Received file for processing. Starting analysis...")

        # 1. Analyze raw structure
        try:
            raw_structure = analyze(full_code_string)
            if not raw_structure:
                self.log(
                    "Analysis returned empty structure. Aborting.", is_error=True)
                return []
            self.log("Raw code structure parsed successfully.")

        except Exception as e:
            self.log(
                f"CRITICAL ERROR during code analysis: {e}", is_error=True)
            return []

        # 2. Flatten functions
        try:
            function_nodes = list(flatten_functions(raw_structure))
            count = len(function_nodes)
            self.log(
                f"Tree traversal complete. Found {count} function(s) to score.")

        except Exception as e:
            self.log(f"Error flattening function tree: {e}", is_error=True)
            return []

        results = []

        # 3. Process loop
        for i, func_node in enumerate(function_nodes, 1):
            self.log("")

            func_name = func_node.get('full_name', 'Unknown')
            self.log(f"[{i}/{count}] Scoring function: '{func_name}'...")

            code = func_node.get('code')
            features = func_node.get('features')

            try:
                score = self.agent.predict(code_str=code, features=features)
                self.log(f"    -> Score for '{func_name}': {score}")

                results.append({
                    "function": func_name,
                    "complexity": score
                })

            except Exception as e:
                self.log(
                    f"    -> ERROR scoring '{func_name}': {e}", is_error=True)
                results.append({
                    "function": func_name,
                    "complexity": None,
                    "error": str(e)
                })

        self.log("")
        self.log("File processing complete. Returning report.")
        return results
