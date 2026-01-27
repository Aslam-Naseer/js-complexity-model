import random


def biased_random(code_string):
    """
    Generate a random float between 1 and 10 (inclusive, 2 decimals)
    with bias based on code string length.

    Args:
        code_string: String of code to analyze

    Returns:
        float: Random number between 1.00 and 10.00
    """
    line_count = len(code_string.strip().split('\n'))
    bias = min(line_count / 50, 1.0)  # 50+ lines = maximum bias

    # bias closer to 1 = higher numbers, closer to 0 = lower numbers
    alpha = 1 + bias * 4  # Range: 1 to 5
    beta_param = 5 - bias * 4  # Range: 5 to 1

    # Generate biased random value between 0 and 1
    biased_value = random.betavariate(alpha, beta_param)

    # Scale to range 1-10 and round to 2 decimals
    result = round(1 + biased_value * 9, 2)
    return result
