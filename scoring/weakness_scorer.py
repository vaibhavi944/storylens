# ====================================================
# FILE PURPOSE
# ====================================================
# A heuristic scoring engine that maps narrative metrics to a weakness
# score. It translates numerical metrics into qualitative labels like
# 'strong', 'moderate', or 'weak'.

from utils.scoring_utils import score_to_label

def score_paragraph(metrics: dict) -> dict:
    """
    Evaluates narrative metrics and returns an overall weakness estimation.
    Higher score = stronger paragraph (less weak).
    """
    score = 0.0
    
    # 1. Pacing (0.0 to 1.0)
    # Good pacing adds to the score
    score += metrics["pacing_score"] * 0.3
    
    # 2. Dialogue Ratio (0.0 to 1.0)
    # Moderate dialogue is good, entirely 0 or entirely 1 might be fine depending on scene
    # We will assume a balanced mix is slightly better for general scenes
    if 0.1 < metrics["dialogue_ratio"] < 0.8:
        score += 0.2
    elif metrics["dialogue_ratio"] > 0:
        score += 0.1
        
    # 3. Emotion (0.0 to 1.0)
    # High emotional charge adds to strength
    score += metrics["emotion_score"] * 0.2
    
    # 4. Hook Strength (0.0 to 1.0)
    score += metrics["hook_strength"] * 0.2
    
    # 5. Repetition Penalty
    # High repetition lowers the score heavily
    score -= (metrics["repetition_score"] * 0.4)
    
    # Normalize final score between 0 and 1
    final_score = max(0.0, min(score + 0.2, 1.0)) # +0.2 baseline bump
    
    label = score_to_label(final_score, threshold_weak=0.4, threshold_strong=0.7)
    
    # Determine the primary issue if weak
    primary_issue = None
    if label != "strong":
        if metrics["repetition_score"] > 0.4:
            primary_issue = "high_repetition"
        elif metrics["emotion_score"] < 0.1:
            primary_issue = "emotionally_flat"
        elif metrics["pacing_score"] < 0.2:
            primary_issue = "poor_pacing"
        elif metrics["dialogue_ratio"] == 0.0 and metrics["avg_sentence_length"] > 20:
            primary_issue = "dense_exposition"
        else:
            primary_issue = "general_weakness"
            
    return {
        "score": final_score,
        "label": label,
        "primary_issue": primary_issue,
        "metrics": metrics
    }
