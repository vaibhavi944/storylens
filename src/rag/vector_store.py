# ====================================================
# FILE PURPOSE
# ====================================================
# Orchestrates the FAISS vector database.
# Handles initialization, saving, loading, and embedding generation
# using the 'intfloat/multilingual-e5-base' model for cross-lingual RAG.

import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from src.utils.logger import get_logger

logger = get_logger(__name__)

VECTOR_STORE_PATH = "vector_stores/faiss_index"

def get_embeddings_model():
    """
    Returns the multilingual embedding model.
    """
    model_name = "intfloat/multilingual-e5-base"
    model_kwargs = {'device': 'cpu'} # Use CPU by default for broader compatibility
    encode_kwargs = {'normalize_embeddings': True}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def save_vector_store(docs: list[Document]):
    """
    Builds and saves a FAISS vector store from a list of documents.
    If a store already exists, it adds to it.
    """
    os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)
    embeddings = get_embeddings_model()
    
    if os.path.exists(VECTOR_STORE_PATH):
        logger.info("Loading existing vector store to add new documents...")
        vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_documents(docs)
    else:
        logger.info("Creating new vector store...")
        vector_store = FAISS.from_documents(docs, embeddings)
        
    vector_store.save_local(VECTOR_STORE_PATH)
    logger.info(f"Vector store saved to {VECTOR_STORE_PATH}")

def load_vector_store() -> FAISS:
    """
    Loads the FAISS vector store from disk.
    Returns None if it doesn't exist.
    """
    if not os.path.exists(VECTOR_STORE_PATH):
        logger.warning(f"Vector store not found at {VECTOR_STORE_PATH}")
        return None
        
    embeddings = get_embeddings_model()
    return FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
