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

def get_similar_strong_examples(query_text: str, language: str = None, k: int = 2) -> list[str]:
    """
    Retrieves top-k similar chunks from the vector store.
    """
    vector_store = load_vector_store()
    if not vector_store:
        logger.warning("Vector store not initialized. Cannot retrieve examples.")
        return []
        
    try:
        # Basic similarity search. In an advanced version, we would pass metadata filters.
        docs = vector_store.similarity_search(query_text, k=k)
        
        # Optionally filter by language post-retrieval if metadata filtering isn't strict
        if language:
            docs = [d for d in docs if d.metadata.get("language", language) == language]
            
        return [d.page_content for d in docs]
    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        return []
