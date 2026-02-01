from agents.orchestrator import ComplexityOrchestrator
from examples import DEFAULT_CODE_SNIPPET
from dotenv import load_dotenv


load_dotenv(override=True)


if __name__ == "__main__":
    import json

    print("--- 1. INITIALIZING SYSTEM ---")
    orchestrator = ComplexityOrchestrator()

    print("\n--- 2. RUNNING PIPELINE ---")
    final_report = orchestrator.process_file(DEFAULT_CODE_SNIPPET)

    print("\n--- 3. FINAL JSON OUTPUT ---")
    print(json.dumps(final_report, indent=2))
