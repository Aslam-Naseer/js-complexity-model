from agents.orchestrator import ComplexityOrchestrator
from dotenv import load_dotenv

load_dotenv(override=True)


if __name__ == "__main__":
    import json

    # 2. The Input Code ("The old foo bar stuff")
    code_input = """
    function foo(a,b) {
        const x = 10;
        const arr = [];

        for (let i = 0; i < a; i++) {
            arr.push(i * x);
        }

        const bar = () => {
            return a+b;
        };

        return {bar, arr}
    }
    """

    print("--- 1. INITIALIZING SYSTEM ---")
    orchestrator = ComplexityOrchestrator()

    print("\n--- 2. RUNNING PIPELINE ---")
    final_report = orchestrator.process_file(code_input)

    print("\n--- 3. FINAL JSON OUTPUT ---")
    print(json.dumps(final_report, indent=2))
