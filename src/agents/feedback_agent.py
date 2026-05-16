# ====================================================
# FILE PURPOSE
# ====================================================
# Agent to generate specific, paragraph-linked feedback using LLM.

import os
from langchain_groq import ChatGroq
from src.prompts.feedback_prompt import FEEDBACK_AGENT_PROMPT
from dotenv import load_dotenv

load_dotenv()

def generate_specific_feedback(text: str, language: str, metrics: dict, weakness: str) -> str:
    """
    Calls the LLM to generate specific, relatable feedback based on the paragraph and its metrics.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        return "Please add your API key to see specific suggestions."

    llm = ChatGroq(temperature=0.4, model_name="llama-3.3-70b-versatile", api_key=api_key)
    
    chain = FEEDBACK_AGENT_PROMPT | llm
    
    try:
        response = chain.invoke({
            "text": text,
            "language": language,
            "weakness": weakness,
            "pacing": metrics.get("pacing_score", 0.5),
            "repetition": metrics.get("repetition_score", 0.0),
            "dialogue": metrics.get("dialogue_ratio", 0.0)
        })
        return response.content.strip()
    except Exception as e:
        return f"Could not generate specific feedback: {e}"
