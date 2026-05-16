# ====================================================
# FILE PURPOSE
# ====================================================
# A heuristic classifier to determine the likely scene type
# (dialogue, action, descriptive, introspective) based on basic
# text features.

from features.dialogue_ratio import calculate_dialogue_ratio
from features.pacing import analyze_pacing

def classify_scene(text: str) -> str:
    """
    Classifies a paragraph into a broad scene type based on heuristics.
    """
    dialogue_ratio = calculate_dialogue_ratio(text)
    pacing_data = analyze_pacing(text)
    
    if dialogue_ratio > 0.4:
        return "dialogue_heavy"
        
    if pacing_data["avg_sentence_length"] > 20:
        return "descriptive_exposition"
        
    if pacing_data["avg_sentence_length"] > 0 and pacing_data["avg_sentence_length"] < 10:
        return "action_oriented"
        
    return "balanced_narration"
