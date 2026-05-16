# ====================================================
# FILE PURPOSE
# ====================================================
# Orchestrates the feature extraction layer.
# Runs all heuristic modules on a given paragraph and returns
# a consolidated dictionary of narrative metrics.

from src.features.dialogue_ratio import calculate_dialogue_ratio
from src.features.pacing import analyze_pacing
from src.features.emotion import analyze_emotion
from src.features.hook_strength import calculate_hook_strength
from src.features.repetition import calculate_repetition_score
from src.features.scene_classifier import classify_scene
from src.utils.language_utils import detect_language

def extract_metrics(paragraph: str, paragraph_id: int = 0) -> dict:
    """
    Extracts a comprehensive set of narrative metrics for a single paragraph.
    """
    lang = detect_language(paragraph)
    
    dialogue_ratio = calculate_dialogue_ratio(paragraph)
    pacing_data = analyze_pacing(paragraph)
    emotion_data = analyze_emotion(paragraph, lang)
    hook_strength = calculate_hook_strength(paragraph)
    repetition_score = calculate_repetition_score(paragraph)
    scene_type = classify_scene(paragraph)
    
    return {
        "paragraph_id": paragraph_id,
        "language": lang,
        "dialogue_ratio": dialogue_ratio,
        "pacing_score": pacing_data["pacing_score"],
        "avg_sentence_length": pacing_data["avg_sentence_length"],
        "emotion_score": emotion_data["emotion_score"],
        "polarity": emotion_data["polarity"],
        "hook_strength": hook_strength,
        "repetition_score": repetition_score,
        "scene_type": scene_type
    }
