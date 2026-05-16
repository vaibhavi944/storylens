# ====================================================
# FILE PURPOSE
# ====================================================
# Applies cleaning rules to raw text data before chunking.
# Ensures formatting is preserved while removing artifacts.

from src.utils.formatting import clean_text

def preprocess_story(raw_text: str) -> str:
    """
    Applies all cleaning rules to a raw story string.
    """
    # Simply delegates to our formatting utility for now
    return clean_text(raw_text)
        