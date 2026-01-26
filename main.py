from code_analyzer.analyzer import analyze

code_str = """
const add = (a, b) => {
    let c = a+b;
    return c;
};
"""


def run_javascript(code: str):
    result = analyze(code)
    if result:
        print("Analysis Result:")
        print(result)
    else:
        print("Failed to analyze code.")


run_javascript(code_str)
