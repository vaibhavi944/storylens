# ====================================================
# FILE PURPOSE
# ====================================================
# Agent to generate personalized overall advice based on analysis.

import os
from langchain_groq import ChatGroq
from src.prompts.summary_prompt import SUMMARY_ADVICE_PROMPT
from dotenv import load_dotenv

load_dotenv()

def generate_overall_advice(results: list[dict], language: str) -> str:
    """
    Calls the LLM to generate a personalized summary based on results.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        return "Please provide an API key to see personalized advice."

    llm = ChatGroq(temperature=0.7, model_name="llama-3.3-70b-versatile", api_key=api_key)
    
    total = len(results)
    strong = sum(1 for p in results if p["label"] == "strong")
    weak = sum(1 for p in results if p["label"] == "weak")
    
    # Collect unique issues
    issues = list(set([p["primary_issue"] for p in results if p["primary_issue"]]))
    issues_str = ", ".join(issues) if issues else "None"
    
    chain = SUMMARY_ADVICE_PROMPT | llm
    
    try:
        response = chain.invoke({
            "total": total,
            "strong": strong,
            "weak": weak,
            "issues": issues_str,
            "language": language
        })
        return response.content.strip()
    except Exception as e:
        return f"Error generating advice: {e}"
