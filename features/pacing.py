# ====================================================
# FILE PURPOSE
# ====================================================
# Analyzes the pacing of a paragraph by evaluating sentence length
# and variance. Rapid variations in sentence length typically indicate
# faster, more dynamic pacing.

import re

def analyze_pacing(text: str) -> dict:
    """
    Calculates average sentence length and sentence length variance.
    A higher variance often means better rhythm and flow.
    """
    if not text:
        return {"avg_sentence_length": 0.0, "variance": 0.0, "pacing_score": 0.0}
        
    # Simple sentence splitting heuristic
    sentences = [s.strip() for s in re.split(r'[.!?।]', text) if s.strip()]
    
    if not sentences:
        return {"avg_sentence_length": 0.0, "variance": 0.0, "pacing_score": 0.0}
        
    lengths = [len(s.split()) for s in sentences]
    avg_len = sum(lengths) / len(lengths)
    
    # Calculate variance
    if len(lengths) > 1:
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
    else:
        variance = 0.0
        
    # Normalize variance into a 0-1 pacing score heuristic
    # High variance = higher pacing score (more dynamic)
    pacing_score = min(variance / 50.0, 1.0) if avg_len < 20 else max(1.0 - (avg_len / 50.0), 0.1)
    
    return {
        "avg_sentence_length": avg_len,
        "variance": variance,
        "pacing_score": pacing_score
    }
