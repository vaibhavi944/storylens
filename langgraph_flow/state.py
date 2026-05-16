# ====================================================
# FILE PURPOSE
# ====================================================
# Defines the typed state dictionary for the LangGraph workflow.
# Tracks the paragraph through analysis, rewrite, and evaluation.

from typing import TypedDict, Optional

class ParagraphState(TypedDict):
    paragraph_id: int
    original_text: str
    language: str
    genre: str

    
    # Feature Extraction
    metrics: Optional[dict]
    score: Optional[float]
    label: Optional[str]
    primary_issue: Optional[str]
    
    # Feedback
    feedback_title: Optional[str]
    feedback_explanation: Optional[str]
    feedback_suggestion: Optional[str]
    
    # Rewrite State
    rewrite_attempts: int
    rewritten_text: Optional[str]
    rewrite_explanation: Optional[str]
    passed_evaluation: bool
