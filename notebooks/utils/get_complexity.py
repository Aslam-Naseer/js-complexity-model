import lizard
import math


def get_complexity_score(js_code):
    """
    Analyzes JS code and returns a normalized 1-10 score.
    """
    analysis = lizard.analyze_file.analyze_source_code("snippet.js", js_code)
    if not analysis.function_list:
        return 1.0

    func = analysis.function_list[0]

    # Heuristic metrics (Cyclomatic, Tokens, Lines)
    cyc = func.cyclomatic_complexity
    tokens = func.token_count
    nloc = func.nloc

    # Logarithmic normalization (spreads out 1-10 range for small code snippets)
    norm_cyc = min(10, (math.log(cyc + 1, 2) * 2.0))
    norm_tokens = min(10, (tokens / 40))
    norm_nloc = min(10, (nloc / 8))

    # Weighted score (50% Logic, 30% Token Density, 20% Physical Size)
    score = (norm_cyc * 0.5) + (norm_tokens * 0.3) + (norm_nloc * 0.2)
    return round(max(1.0, min(10.0, score)), 1)


def get_complexity_label(score):
    """
    Maps a numeric 1-10 score to a qualitative label.
    Standard industry thresholds (McCabe/Sonar).
    """
    if score <= 3.0:
        return "Simple"
    elif score <= 6.0:
        return "Moderate"
    elif score <= 8.5:
        return "Complex"
    else:
        return "Critical"
