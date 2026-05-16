# ====================================================
# FILE PURPOSE
# ====================================================
# Detects repetitive vocabulary within a paragraph.
# High repetition without poetic intent usually indicates weak writing.

from collections import Counter
import re

def calculate_repetition_score(text: str) -> float:
    """
    Returns a score from 0.0 to 1.0 representing vocabulary repetitiveness.
    Ignores common stop words (very basic heuristic here).
    """
    if not text:
        return 0.0
        
    # Basic tokenization, lowercasing, and removing punctuation
    words = re.findall(r'\b\w+\b', text.lower())
    
    if len(words) < 10:
        return 0.0 # Too short to judge repetition fairly
        
    # A tiny list of common stopwords to ignore
    stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "is", "was", "were", "it", "he", "she", "they", "i", "you"}
    filtered_words = [w for w in words if w not in stopwords]
    
    if not filtered_words:
        return 0.0
        
    word_counts = Counter(filtered_words)
    most_common = word_counts.most_common(1)[0][1]
    
    # If the most common non-stopword appears many times relative to length, it's repetitive
    ratio = most_common / len(filtered_words)
    
    # Normalize (e.g., if ratio > 0.1, it starts getting repetitive)
    score = min(ratio * 5.0, 1.0)
    
    return score
