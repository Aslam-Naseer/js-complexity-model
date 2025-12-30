import re


def preprocess_js_code(datapoint, max_len=2000):
    code = datapoint.get("original_string", "")

    code = code.strip()
    code = re.sub(r"\s+", " ", code)
    if len(code) > max_len:
        code = code[:max_len]

    return code
