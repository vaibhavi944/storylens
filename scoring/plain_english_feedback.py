# ====================================================
# FILE PURPOSE
# ====================================================
# Translates technical narrative metrics and weakness classifications
# into human-readable, writer-friendly feedback. Avoids jargon.

def get_feedback_for_issue(issue: str, metrics: dict) -> dict:
    """
    Returns a writer-friendly explanation of the issue and a suggestion.
    """
    feedback_map = {
        "high_repetition": {
            "title": "Repetitive Phrasing",
            "explanation": "This section relies heavily on the same words or sentence structures.",
            "suggestion": "Try varying your vocabulary or combining sentences to create a smoother flow."
        },
        "emotionally_flat": {
            "title": "Emotionally Flat",
            "explanation": "The tone here feels a bit neutral or detached.",
            "suggestion": "Consider weaving in the character's internal feelings or sensory details to help readers connect."
        },
        "poor_pacing": {
            "title": "Monotonous Pacing",
            "explanation": "The sentences in this section are very similar in length, which can make the reading experience feel flat.",
            "suggestion": "Try breaking up longer sentences or adding a short, punchy sentence to create rhythm."
        },
        "dense_exposition": {
            "title": "Heavy Description",
            "explanation": "This block is heavily descriptive without any breaks.",
            "suggestion": "Adding a short line of dialogue or breaking this into smaller paragraphs can help readers stay engaged."
        },
        "general_weakness": {
            "title": "Attention Drift",
            "explanation": "This section might cause the reader's attention to drift.",
            "suggestion": "Look for ways to tighten the prose, clarify the action, or raise the stakes."
        }
    }
    
    return feedback_map.get(issue, {
        "title": "Strong Section",
        "explanation": "This part reads well.",
        "suggestion": "No major changes needed."
    })
