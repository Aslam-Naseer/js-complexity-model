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

        return {"success": True, "data": json.loads(result.stdout)}

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip().split(
            '\n')[0] if e.stderr else "Unknown error"
        return {
            "success": False,
            "error": error_message,
            "exit_code": e.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
