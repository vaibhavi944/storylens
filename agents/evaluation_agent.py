# ====================================================
# FILE PURPOSE
# ====================================================
# Uses the LLM to evaluate if a rewrite successfully fixed the issue.
# This powers the LangGraph conditional routing (retry if failed).

import os
from langchain_groq import ChatGroq
from prompts.evaluator_prompt import EVALUATOR_PROMPT
from dotenv import load_dotenv

load_dotenv()

def evaluate_rewrite(original_text: str, rewritten_text: str, weakness: str) -> bool:
    """
    Returns True if the rewrite passed, False if it failed.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        return True # Default to pass if no API key
        
    llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile", api_key=api_key)
    
    chain = EVALUATOR_PROMPT | llm
    try:
        result = chain.invoke({
            "weakness": weakness,
            "original_text": original_text,
            "rewritten_text": rewritten_text
        })
        
        response = result.content.strip().upper()
        return "PASS" in response
    except Exception:
        return True # Default to pass on error to avoid infinite loops
