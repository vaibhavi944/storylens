# ====================================================
# FILE PURPOSE
# ====================================================
# Defines the system prompts for the rewriting engine.
# Ensures the LLM preserves the author's tone, language, and POV
# while addressing the specific narrative weakness.

from langchain_core.prompts import PromptTemplate

REWRITE_PROMPT = PromptTemplate.from_template(
    """You are an expert fiction editor.
Your goal is to rewrite the following paragraph to fix a specific narrative weakness,
while strictly preserving the author's original tone, language, and point of view (POV).

Original Text:
{original_text}

Language: {language}
Identified Weakness: {weakness}
Explanation of Issue: {explanation}

Strong Example(s) for Inspiration (do not copy these, just observe the style/pacing):
{examples}

Task:
Provide an improved version of the text that fixes the weakness. Do not add any conversational filler.
Return ONLY the rewritten text.
"""
)

EXPLANATION_PROMPT = PromptTemplate.from_template(
    """You are a gentle, encouraging fiction editor.
Briefly explain to the writer what changed between their original text and the rewritten version,
and why it improves the {weakness}.

Original: {original_text}
Rewrite: {rewritten_text}
Language: {language}

Rules:
- Speak directly to the writer in an encouraging tone.
- Use plain language. No technical jargon. NO mentions of "embeddings", "vector similarity", "RAG", "polarity scores", etc.
- Keep it under 3 sentences.
- IMPORTANT: You MUST write this explanation in the SAME LANGUAGE as the story ({language}). If the story is in Hindi, explain in Hindi. If Marathi, explain in Marathi.
"""
)
