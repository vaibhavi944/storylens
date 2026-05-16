# ====================================================
# FILE PURPOSE
# ====================================================
# Core agent that orchestrates the rewrite process.
# Calls the Groq LLM using the Rewrite prompts and integrates
# the retrieved examples.

import os
from langchain_groq import ChatGroq
from prompts.rewrite_prompt import REWRITE_PROMPT, EXPLANATION_PROMPT
from rag.retriever import get_similar_strong_examples
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        return None
    return ChatGroq(temperature=0.7, model_name="llama-3.3-70b-versatile", api_key=api_key)

def generate_rewrite(original_text: str, language: str, weakness: str, explanation: str, genre: str = "General") -> dict:
    llm = get_llm()
    if not llm:
        return {"rewrite": original_text, "explanation": "API Key missing. Cannot generate rewrite."}
        
    # Real retrieval-backed rewriting: Use genre and language for better context
    examples = get_similar_strong_examples(original_text, language=language, genre=genre, k=2)
    examples_text = "\n\n".join(examples) if examples else "None available."

    
    # Generate Rewrite
    rewrite_chain = REWRITE_PROMPT | llm
    rewrite_result = rewrite_chain.invoke({
        "original_text": original_text,
        "language": language,
        "weakness": weakness,
        "explanation": explanation,
        "examples": examples_text
    })
    rewritten_text = rewrite_result.content.strip()
    
    # Generate Explanation
    explanation_chain = EXPLANATION_PROMPT | llm
    explanation_result = explanation_chain.invoke({
        "original_text": original_text,
        "rewritten_text": rewritten_text,
        "weakness": weakness,
        "language": language
    })
    
    return {
        "rewrite": rewritten_text,
        "explanation": explanation_result.content.strip()
    }
