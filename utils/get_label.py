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
