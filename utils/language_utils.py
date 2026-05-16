# ====================================================
# FILE PURPOSE
# ====================================================
# Provides utilities for detecting the language of the text.
# Supports the primary languages of StoryLens: English, Hindi, and Marathi.

from langdetect import detect, LangDetectException
from utils.logger import get_logger

logger = get_logger(__name__)

def detect_language(text: str) -> str:
    """
    Detects the language of the given text.
    Returns 'english', 'hindi', 'marathi', or 'unknown'.
    """
    if not text or len(text.strip()) == 0:
        return 'unknown'
        
    try:
        lang_code = detect(text)
        if lang_code == 'en':
            return 'english'
        elif lang_code == 'hi':
            return 'hindi'
        elif lang_code == 'mr':
            return 'marathi'
        else:
            return 'unknown'
    except LangDetectException as e:
        logger.warning(f"Language detection failed: {e}")
        return 'unknown'
