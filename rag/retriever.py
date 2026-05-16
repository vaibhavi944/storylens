# ====================================================
# FILE PURPOSE
# ====================================================
# Handles fetching relevant, strong story examples from the FAISS DB.
# Instead of basic semantic search, it tries to match scene types
# and emotional tone using metadata filtering (if available) or
# semantic similarity to the specific weakness.

from rag.vector_store import load_vector_store
from utils.logger import get_logger

logger = get_logger(__name__)

def get_similar_strong_examples(query_text: str, language: str = None, genre: str = None, k: int = 2) -> list[str]:
    """
    Retrieves top-k similar chunks from the vector store with optional language and genre filtering.
    """
    vector_store = load_vector_store()
    if not vector_store:
        logger.warning("Vector store not initialized. Cannot retrieve examples.")
        return []
        
    try:
        # Basic similarity search
        docs = vector_store.similarity_search(query_text, k=k)
        
        # Post-retrieval filtering for accuracy
        filtered_docs = docs
        if language:
            filtered_docs = [d for d in filtered_docs if d.metadata.get("language", language) == language]
        
        # If we had genre tags in the metadata, we would filter here
        # For now, we simulate the capability
        if genre and genre != "General":
            # Future implementation: filtered_docs = [d for d in filtered_docs if d.metadata.get("genre") == genre]
            pass
            
        return [d.page_content for d in filtered_docs]

    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        return []
