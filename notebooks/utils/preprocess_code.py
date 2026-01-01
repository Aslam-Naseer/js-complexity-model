import re


def preprocess_js_code(datapoint, max_len=2000):
    code = datapoint.get("code", "")

    code = code.strip()
    code = re.sub(r"\s+", " ", code)
    if len(code) > max_len:
        code = code[:max_len]

    return code


def convert_to_arrow(js_code):
    pattern = r"(async\s+)?function\s*([a-zA-Z0-9_$]+)?\s*\((.*?)\)\s*\{"

    def replace_func(match):
        is_async = match.group(1) if match.group(1) else ""
        name = match.group(2)
        params = match.group(3)

        if name:
            return f"const {name} = {is_async}({params}) => {{"
        else:
            return f"{is_async}({params}) => {{"

    return re.sub(pattern, replace_func, js_code)
