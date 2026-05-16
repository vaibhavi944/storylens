# ====================================================
# FILE PURPOSE
# ====================================================
# Extracts the ratio of dialogue to narration within a paragraph.
# Uses quotation marks and language-specific dialogue markers to
# estimate how much of the text is conversational.

import re

def calculate_dialogue_ratio(text: str) -> float:
    """
    Calculates the ratio of characters inside dialogue quotes vs total characters.
    Supports standard double/single quotes and common typographical quotes.
    """
    if not text or len(text.strip()) == 0:
        return 0.0
        
    # Match text within quotes (", ', “, ”, ‘, ’)
    # This is a heuristic approach and might catch some quoted thoughts as well
    dialogue_pattern = r'["“”\'‘’](.*?)["“”\'‘’]'
    matches = re.findall(dialogue_pattern, text)
    
    dialogue_length = sum(len(m) for m in matches)
    total_length = len(text)
    
    if total_length == 0:
        return 0.0
        
    ratio = dialogue_length / total_length
    return min(ratio, 1.0)
