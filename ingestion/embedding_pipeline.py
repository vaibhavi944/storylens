# ====================================================
# FILE PURPOSE
# ====================================================
# End-to-end pipeline to read raw datasets, preprocess, chunk,
# tag with metadata, and store into the FAISS vector DB.

import os
import json
import random
from ingestion.preprocess import preprocess_story
from ingestion.chunking import chunk_text
from rag.vector_store import save_vector_store
from langchain_core.documents import Document
from utils.logger import get_logger

logger = get_logger(__name__)

GENRES = ["General", "Romance", "Thriller", "Fantasy", "Drama"]

def process_file(filepath: str, lang: str, max_docs: int = 500):
    """
    Reads a JSONL file, chunks it, and creates Document objects with genre tags.
    """
    docs = []
    logger.info(f"Processing file: {filepath}")
    
    if not os.path.exists(filepath):
        logger.warning(f"File not found: {filepath}")
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= max_docs:
                break
                
            try:
                data = json.loads(line)
                text = data.get("text", "")
                
                cleaned_text = preprocess_story(text)
                chunks = chunk_text(cleaned_text)
                
                # Randomly assign a genre for this demo dataset
                # In a real app, we'd use an LLM classifier or pre-tagged data
                assigned_genre = random.choice(GENRES)
                
                for chunk in chunks:
                    metadata = {
                        "source": os.path.basename(filepath),
                        "language": lang,
                        "genre": assigned_genre,
                        "chunk_length": len(chunk)
                    }
                    docs.append(Document(page_content=chunk, metadata=metadata))
            except Exception as e:
                logger.warning(f"Failed to process line {i} in {filepath}: {e}")
                
    return docs

def run_pipeline():
    logger.info("Starting full embedding pipeline...")
    
    # Define paths
    en_path = "data/raw_stories/english/tinystories_1000.jsonl"
    hi_path = "data/raw_stories/hindi/hindi_iitb_1000.jsonl"
    
    all_docs = []
    
    # Process English
    all_docs.extend(process_file(en_path, "english", max_docs=500))
    
    # Process Hindi
    all_docs.extend(process_file(hi_path, "hindi", max_docs=500))
                
    if all_docs:
        logger.info(f"Generated {len(all_docs)} chunks. Building/Updating vector store...")
        save_vector_store(all_docs)
    else:
        logger.warning("No documents found to process.")

if __name__ == "__main__":
    run_pipeline()
