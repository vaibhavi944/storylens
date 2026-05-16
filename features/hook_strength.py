# ====================================================
# FILE PURPOSE
# ====================================================
# Estimates the hook strength of a paragraph.
# A strong hook often contains questions, strong emotional words,
# or short, punchy opening sentences.

import re

def calculate_hook_strength(text: str) -> float:
    """
    Returns a heuristic score between 0.0 and 1.0 indicating hook strength.
    Looks for question marks, exclamation marks, and short initial sentences.
    """
    if not text:
        return 0.0
        
    score = 0.0
    
    # Questions naturally hook readers
    if '?' in text:
        score += 0.3
        
    # Exclamations show high energy
    if '!' in text:
        score += 0.2
        
    sentences = [s.strip() for s in re.split(r'[.!?।]', text) if s.strip()]
    if sentences:
        first_sentence_len = len(sentences[0].split())
        # Short punchy first sentence is a strong hook
        if first_sentence_len < 8:
            score += 0.3
        elif first_sentence_len < 15:
            score += 0.1
            
    return min(score, 1.0)
