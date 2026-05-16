# ====================================================
# FILE PURPOSE
# ====================================================
# Extracts the emotional polarity and subjectivity of a paragraph.
# Uses TextBlob as a lightweight heuristic to determine if a section
# is emotionally flat or highly charged.

from textblob import TextBlob
from src.utils.logger import get_logger

logger = get_logger(__name__)

def analyze_emotion(text: str, language: str = 'english') -> dict:
    """
    Calculates emotional polarity (-1.0 to 1.0) and subjectivity (0.0 to 1.0).
    Note: TextBlob works best on English. For other languages, it may be
    less accurate unless translated first, but we use it as a basic heuristic.
    """
    if not text:
        return {"polarity": 0.0, "subjectivity": 0.0, "emotion_score": 0.0}
        
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Absolute polarity as a measure of "emotional charge" (0 to 1)
        emotion_score = abs(polarity)
        
        return {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "emotion_score": emotion_score
        }
    except Exception as e:
        logger.warning(f"Emotion analysis failed: {e}")
        return {"polarity": 0.0, "subjectivity": 0.0, "emotion_score": 0.0}
