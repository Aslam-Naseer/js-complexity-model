import subprocess
import json


def pretty_print_json(json_string: str, indent: int = 2) -> None:
    """
    Takes a JSON string and prints it in a readable, formatted way.
    """
    try:
        parsed = json.loads(json_string)
        print(json.dumps(parsed, indent=indent, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print("Invalid JSON string:")
        print(e)


def run_javascript(code: str):
    try:

        result = subprocess.run(
            ["node", "code_analyzer/wrapper.js", code],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("Error executing JavaScript code:")
            print(result.stderr)
            return

        pretty_print_json(result.stdout)

    except Exception as e:
        print("Error:", e)


# run_javascript()
