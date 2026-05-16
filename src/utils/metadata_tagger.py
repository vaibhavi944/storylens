# ====================================================
# FILE PURPOSE
# ====================================================
# Provides an LLM-based metadata tagging system to automatically infer
# metadata for story chunks. This ensures high-quality RAG retrieval
# by filtering on metadata like genre, emotional tone, and scene type.

import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

class StoryMetadata(BaseModel):
    genre: str = Field(description="The primary genre of the story chunk (e.g., romance, thriller, fantasy, slice of life).")
    emotional_tone: str = Field(description="The dominant emotional tone (e.g., tense, joyful, melancholic, neutral).")
    scene_type: str = Field(description="The type of scene (e.g., action, dialogue, exposition, introspective, descriptive).")
    pacing_style: str = Field(description="The pacing of the scene (e.g., fast, moderate, slow).")
    dialogue_density: str = Field(description="The density of dialogue in the scene (e.g., high, low, none).")
    language: str = Field(description="The language of the text (e.g., english, hindi, marathi).")

def get_metadata_tagger_llm():
    """
    Initializes the ChatGroq LLM for metadata tagging.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        logger.warning("GROQ_API_KEY is missing or invalid. Metadata tagging will return default values.")
        return None
        
    return ChatGroq(
        temperature=0,
        model_name="llama-3.3-70b-versatile",
        api_key=api_key
    )

def tag_text(text: str) -> dict:
    """
    Analyzes text and returns structured metadata using the LLM.
    Falls back to default values if the LLM is unavailable or fails.
    """
    llm = get_metadata_tagger_llm()
    if not llm:
        return {
            "genre": "unknown",
            "emotional_tone": "neutral",
            "scene_type": "exposition",
            "pacing_style": "moderate",
            "dialogue_density": "low",
            "language": "unknown"
        }
    
    try:
        structured_llm = llm.with_structured_output(StoryMetadata)
        prompt = f"Analyze the following story excerpt and extract its metadata:\n\n{text}"
        result = structured_llm.invoke(prompt)
        return result.dict()
    except Exception as e:
        logger.error(f"Failed to extract metadata: {e}")
        return {
            "genre": "unknown",
            "emotional_tone": "neutral",
            "scene_type": "exposition",
            "pacing_style": "moderate",
            "dialogue_density": "low",
            "language": "unknown"
        }
