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
    # Balanced pacing is critical for professional writing
    score += metrics["pacing_score"] * 0.4
    
    # 2. Dialogue Ratio (0.0 to 1.0)
    if 0.1 < metrics["dialogue_ratio"] < 0.6:
        score += 0.2
    elif metrics["dialogue_ratio"] > 0:
        score += 0.1
        
    # 3. Emotion (0.0 to 1.0)
    score += metrics["emotion_score"] * 0.3
    
    # 4. Hook Strength (0.0 to 1.0)
    score += metrics["hook_strength"] * 0.3
    
    # 5. Repetition Penalty
    # Repetition is now a more balanced heuristic
    score -= (metrics["repetition_score"] * 0.5)
    
    # Normalize final score between 0 and 1
    # Baseline bump increased to 0.4 to assume "Strong/Moderate" by default
    final_score = max(0.0, min(score + 0.4, 1.0)) 
    
    # Adjusted thresholds: 0.6+ is now Strong (was 0.7)
    label = score_to_label(final_score, threshold_weak=0.35, threshold_strong=0.6)
    
    # Determine the primary issue if weak or moderate
    primary_issue = None
    if label != "strong":
        if metrics["repetition_score"] > 0.3:
            primary_issue = "high_repetition"
        elif metrics["emotion_score"] < 0.15:
            primary_issue = "emotionally_flat"
        elif metrics["pacing_score"] < 0.2:
            primary_issue = "poor_pacing"
        elif metrics["dialogue_ratio"] == 0.0 and metrics["avg_sentence_length"] > 25:
            primary_issue = "dense_exposition"
        else:
            primary_issue = "general_weakness"

            
    return {
        "score": final_score,
        "label": label,
        "primary_issue": primary_issue,
        "metrics": metrics
    }
