# ====================================================
# FILE PURPOSE
# ====================================================
# Generates intentionally flawed story chapters for demo purposes.
# Supports English, Hindi, and Marathi narratives across different genres.
# Highlights specific narrative weaknesses to be caught by the StoryLens system.

import os
import json
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

WEAKNESSES = [
    "weak pacing", 
    "repetitive narration", 
    "low dialogue", 
    "emotionally flat sections", 
    "weak hooks", 
    "excessive exposition"
]

GENRES = ["romance", "thriller", "family drama", "fantasy", "slice of life"]
LANGUAGES = ["english", "hindi", "marathi"]

def generate_demo_story(language: str, genre: str, weakness: str) -> str:
    """
    Generates a story chapter with a specific intentionally embedded weakness.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        logger.error("GROQ_API_KEY is missing. Cannot generate demo inputs.")
        return "Error: GROQ_API_KEY missing."

    llm = ChatGroq(
        temperature=0.7,
        model_name="llama-3.3-70b-versatile",
        api_key=api_key
    )

    prompt = PromptTemplate.from_template(
        "You are an amateur writer writing a {genre} story chapter in {language}. "
        "Write a 3-paragraph scene (around 300 words). "
        "Intentionally include the following narrative weakness: {weakness}. "
        "Make it obvious that it suffers from this weakness, but still readable. "
        "Return ONLY the story text, no explanations."
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({
            "language": language,
            "genre": genre,
            "weakness": weakness
        })
        return response.content.strip()
    except Exception as e:
        logger.error(f"Error generating demo story: {e}")
        return f"Error generating story: {e}"

def generate_all_demos():
    """
    Generates demo inputs for all combinations and saves them to disk.
    """
    output_dir = "data/demo_inputs"
    for lang in LANGUAGES:
        lang_dir = os.path.join(output_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        for genre in GENRES[:2]: # Limit to 2 genres to save API calls
            for weakness in WEAKNESSES[:2]: # Limit to 2 weaknesses
                logger.info(f"Generating: {lang} - {genre} - {weakness}")
                story = generate_demo_story(lang, genre, weakness)
                
                filename = f"{genre.replace(' ', '_')}_{weakness.replace(' ', '_')}.txt"
                filepath = os.path.join(lang_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(story)
                logger.info(f"Saved {filepath}")

if __name__ == "__main__":
    generate_all_demos()
