# ====================================================
# FILE PURPOSE
# ====================================================
# Provides formatting utilities to clean strings, maintain
# paragraph structure, and avoid breaking literary formatting
# like dialogue tags.

import re

def clean_text(text: str) -> str:
    """
    Cleans malformed spacing and broken line breaks without destroying
    dialogue formatting or paragraph structures.
    """
    if not text:
        return ""
        
    # Replace multiple spaces with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Normalize line endings to \n
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Replace 3 or more newlines with double newlines (to preserve paragraphs)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def split_into_paragraphs(text: str) -> list[str]:
    """
    Splits text into paragraphs based on double newlines.
    """
    cleaned = clean_text(text)
    paragraphs = [p.strip() for p in cleaned.split('\n\n') if p.strip()]
    return paragraphs
