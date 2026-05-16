# ====================================================
# FILE PURPOSE
# ====================================================
# Provides mapping utilities for converting numerical heuristic
# scores into human-readable labels ("strong", "moderate", "weak")
# and corresponding UI colors ("green", "yellow", "red").

def score_to_label(score: float, threshold_weak: float = 0.3, threshold_strong: float = 0.7) -> str:
    """
    Converts a normalized numerical score (0.0 to 1.0) into a qualitative label.
    """
    if score >= threshold_strong:
        return "strong"
    elif score >= threshold_weak:
        return "moderate"
    else:
        return "weak"

def label_to_color(label: str) -> str:
    """
    Maps a weakness label to a UI color.
    """
    mapping = {
        "strong": "green",
        "moderate": "yellow",
        "weak": "red"
    }
    return mapping.get(label, "grey")
