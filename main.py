import subprocess
import json


def run_javascript():
    res = subprocess.run(
        ['node', 'code_analyzer/index.js'],
        capture_output=True,
        text=True
    )

    print("STDOUT:", res.stdout)


run_javascript()
