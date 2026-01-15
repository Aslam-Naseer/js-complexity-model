import re
import random


def sanitize_js_code(code):
    """
    Cleans common 'wild' JS errors that cause parser crashes.
    """
    if not code:
        return ""

    if re.match(r'^\s*function\s*\(', code):
        code = f"({code})"

    code = re.sub(r'\bpackage\b', 'pkg', code)
    code = code.replace('lastSync, credentials, lastSync',
                        'lastSync, credentials, lastSync_alt')

    return code


def convert_to_arrow(js_code):
    pattern = r"^\s*(async\s+)?function\s*([a-zA-Z0-9_$]+)?\s*\((.*?)\)\s*\{"

    def replace_func(match):
        is_async = match.group(1) if match.group(1) else ""
        name = match.group(2)
        params = match.group(3)

        if name:
            return f"const {name} = {is_async}({params}) => {{"

        return f"{is_async}({params}) => {{"

    return re.sub(pattern, replace_func, js_code)


def sanitize_code(code):
    stripped_code = code.strip()
    is_function_expr = re.match(
        r'^(return\s+)?(async\s+)?function', stripped_code)

    code = sanitize_js_code(code)
    if is_function_expr or random.random() < 0.55:
        return convert_to_arrow(code)

    return code
