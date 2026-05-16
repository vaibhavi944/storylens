# ====================================================
# FILE PURPOSE
# ====================================================
# Defines the system prompt for evaluating a rewrite.

from langchain_core.prompts import PromptTemplate

EVALUATOR_PROMPT = PromptTemplate.from_template(
    """You are an expert fiction editor.
Evaluate if the following rewritten text successfully fixed the original weakness without losing the author's tone.

Original Weakness: {weakness}
Original Text: {original_text}
Rewritten Text: {rewritten_text}

Return "PASS" if the rewrite is good and fixes the issue.
Return "FAIL" if the rewrite is still weak, unnatural, or completely loses the author's original voice.
Return ONLY "PASS" or "FAIL".
"""
)
