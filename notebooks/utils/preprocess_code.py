import re


def preprocess_js_code(datapoint, max_len=2000):
    code = datapoint.get("original_string", "")

    code = code.strip()
    code = re.sub(r"\s+", " ", code)
    if len(code) > max_len:
        code = code[:max_len]

    return code


def convert_to_arrow(js_code):
    pattern = r"function\s+([a-zA-Z0-9_$]+)\s*\((.*?)\)\s*\{"
    replacement = r"const \1 = (\2) => {"

    return re.sub(pattern, replacement, js_code)
