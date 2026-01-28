import subprocess
import json


def analyze(code: str):
    try:
        result = subprocess.run(
            ["node", "code_analyzer/bridge.js", code],
            capture_output=True,
            text=True,
            check=True
        )

        if result.returncode != 0:
            print(result.stderr)
            return None

        return json.loads(result.stdout)

    except Exception as e:
        print("Error:", e)
        return None
