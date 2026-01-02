import re
import random


def sanitize_js_code(code):
    """
    Cleans common 'wild' JS errors that cause parser crashes.
    """
    if not code:
        return ""

    # 1. Fix Anonymous Functions at start of string
    # Change 'function(...) {' to '(function(...) {' so it's a valid expression
    if re.match(r'^\s*function\s*\(', code):
        code = f"({code})"

    # 2. Fix Reserved Keyword 'package'
    # Replaces 'package' with 'pkg' only when used as a variable/parameter
    # \b ensures we don't hit words like 'packages' or 'repackage'
    code = re.sub(r'\bpackage\b', 'pkg', code)

    # 3. Fix Duplicate Argument 'lastSync'
    # Finds instances where 'lastSync, credentials, lastSync' occurs in params
    # This is a specific fix for the AppUserModel error in your logs
    code = code.replace('lastSync, credentials, lastSync',
                        'lastSync, credentials, lastSync_alt')

    # 4. Handle JSX (Basic Mitigation)
    # Most standard linters fail on '<'. If we detect JSX and aren't using a
    # JSX parser, these will always fail. For now, we leave them, but
    # identifying them helps debug.

    return code


def convert_to_arrow(js_code):
    # Added ^\s* to ensure it only matches if the code STARTS with this pattern
    # Removed (return\s+)? because if it starts with 'return', it's not a top-level function declaration
    pattern = r"^\s*(async\s+)?function\s*([a-zA-Z0-9_$]+)?\s*\((.*?)\)\s*\{"

    def replace_func(match):
        # We keep the groups as they were, but prefix is now always empty
        # because a string starting with 'return' won't match this pattern.
        is_async = match.group(1) if match.group(1) else ""
        name = match.group(2)
        params = match.group(3)

        if name:
            return f"const {name} = {is_async}({params}) => {{"

        return f"{is_async}({params}) => {{"

    # Use re.sub with the anchored pattern
    return re.sub(pattern, replace_func, js_code)


def sanitize_code(code):
    stripped_code = code.strip()
    is_function_expr = re.match(
        r'^(return\s+)?(async\s+)?function', stripped_code)

    code = sanitize_js_code(code)
    if is_function_expr or random.random() < 0.55:
        return convert_to_arrow(code)

    return code


def preprocess_js_code(original_code, max_len=2000):

    code = original_code.strip()
    code = re.sub(r"\s+", " ", code)

    if len(code) > max_len:
        code = code[:max_len]

    return code
