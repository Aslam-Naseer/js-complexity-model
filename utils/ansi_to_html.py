import re


def ansi_to_html(text):
    # Map ANSI codes to HTML colors
    ansi_map = {
        '\033[91m': '<span style="color: #ff5f5f; font-weight: bold;">',  # Red
        '\033[92m': '<span style="color: #5fff5f; font-weight: bold;">',  # Green
        '\033[93m': '<span style="color: #ffff5f; font-weight: bold;">',  # Yellow
        '\033[94m': '<span style="color: #5f5fff; font-weight: bold;">',  # Blue
        '\033[95m': '<span style="color: #ff5fff; font-weight: bold;">',  # Magenta
        '\033[96m': '<span style="color: #00ffff; font-weight: bold;">',  # Cyan
        '\033[0m': '</span>'
    }

    # Replace ANSI codes with HTML spans
    for code, html in ansi_map.items():
        text = text.replace(code, html)

    # Clean up any leftover weird codes just in case
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    return text
