# ====================================================
# FILE PURPOSE
# ====================================================
# End-to-end pipeline to read raw datasets, preprocess, chunk,
# optionally tag with metadata, and store into the FAISS vector DB.

import os
import json
from ingestion.preprocess import preprocess_story
from ingestion.chunking import chunk_text
from rag.vector_store import save_vector_store
from utils.metadata_tagger import tag_text
from langchain_core.documents import Document
from utils.logger import get_logger

logger = get_logger(__name__)

def process_file(filepath: str, max_docs: int = 50):
    """
    Reads a JSONL file, chunks it, and creates Document objects.
    Limited to max_docs to avoid massive API/processing costs during setup.
    """
    docs = []
    logger.info(f"Processing file: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= max_docs:
                break
                
            try:
                data = json.loads(line)
                text = data.get("text", "")
                base_lang = data.get("language", "unknown")
                
                cleaned_text = preprocess_story(text)
                chunks = chunk_text(cleaned_text)
                
                for chunk in chunks:
                    # In a full production run, we might tag every chunk via LLM.
                    # For this pipeline, we use heuristic metadata to save costs.
                    # However, we'll try tagging the first chunk of every story.
                    # Here, we just store basic metadata.
                    metadata = {
                        "source": os.path.basename(filepath),
                        "language": base_lang,
                        "chunk_length": len(chunk)
                    }
                    
                    docs.append(Document(page_content=chunk, metadata=metadata))
            except Exception as e:
                logger.warning(f"Failed to process line {i} in {filepath}: {e}")
                
    return docs

def run_pipeline():
    logger.info("Starting embedding pipeline...")
    raw_dirs = [
        "data/raw_stories/english",
        "data/raw_stories/hindi",
        "data/raw_stories/marathi"
    ]
    
    all_docs = []
    
    for d in raw_dirs:
        if not os.path.exists(d):
            continue
        for filename in os.listdir(d):
            if filename.endswith(".jsonl"):
                filepath = os.path.join(d, filename)
                docs = process_file(filepath, max_docs=20) # Small limit for quick setup
                all_docs.extend(docs)
                
    if all_docs:
        logger.info(f"Generated {len(all_docs)} chunks. Building vector store...")
        save_vector_store(all_docs)
    else:
        logger.warning("No documents found to process.")

if __name__ == "__main__":
    run_pipeline()
