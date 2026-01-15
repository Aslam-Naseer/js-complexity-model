from .sanitize_code import sanitize_code

SYSTEM_PROMPT = "You are a static analysis expert. Analyze the code metrics and calculate the cyclomatic complexity."


def get_messages(code: str) -> list[dict[str, str]]:
    sanitized_code = sanitize_code(code)

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },    {
            "role": "user",
            "content": sanitized_code
        }
    ]
