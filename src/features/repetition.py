# ====================================================
# FILE PURPOSE
# ====================================================
# Detects repetitive vocabulary within a paragraph.
# High repetition without poetic intent usually indicates weak writing.

from collections import Counter
import re

import re
from collections import Counter

def calculate_repetition_score(text: str) -> float:
    """
    Evaluates repetitiveness using sentence starts, word frequency, and bigrams.
    Returns a score from 0.0 to 1.0 (Higher = More repetitive).
    """
    if not text or len(text.split()) < 10:
        return 0.0

    # 1. Sentence Start Analysis (Common amateur mistake: "He... He... He...")
    sentences = [s.strip() for s in re.split(r'[.!?।]', text) if s.strip()]
    if len(sentences) > 2:
        starts = [s.split()[0].lower() for s in sentences if len(s.split()) > 0]
        start_counts = Counter(starts)
        most_common_start = start_counts.most_common(1)[0][1]
        start_score = (most_common_start / len(sentences)) if len(sentences) > 0 else 0
    else:
        start_score = 0.0

    # 2. Word Frequency (Excluding common structural words)
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "is", "was", "were", "it", "he", "she", "they", "i", "you", "of", "with"}
    filtered_words = [w for w in words if w not in stopwords]
    
    word_freq_score = 0.0
    if filtered_words:
        word_counts = Counter(filtered_words)
        # Look for words appearing more than 3 times or more than 15% of the text
        repeat_count = sum(1 for count in word_counts.values() if count > 2)
        word_freq_score = min(repeat_count / (len(filtered_words) / 5), 1.0)

    # 3. Bigram Repetition (Repeating phrases)
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    bigram_counts = Counter(bigrams)
    repeat_bigrams = sum(1 for count in bigram_counts.values() if count > 1)
    bigram_score = min(repeat_bigrams / (len(words) / 10), 1.0)

    # Weighted Average
    # Sentence starts are a high-signal indicator of "amateur" repetition
    final_score = (start_score * 0.5) + (word_freq_score * 0.25) + (bigram_score * 0.25)
    
    return min(final_score, 1.0)

