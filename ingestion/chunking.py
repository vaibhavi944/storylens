# ====================================================
# FILE PURPOSE
# ====================================================
# Prepares text chunks using a strategy optimized for narrative fiction.
# Chunking is based on paragraphs and scene boundaries rather than
# arbitrary fixed lengths.

from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_narrative_splitter(chunk_size: int = 700, chunk_overlap: int = 120):
    """
    Returns a text splitter configured to respect paragraph and sentence
    boundaries, making chunks semantically meaningful.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n\n", "\n\n", "\n", "।", ".", "?", "!", " ", ""],
        keep_separator=True
    )

def chunk_text(text: str) -> list[str]:
    """
    Splits text into chunks.
    """
    splitter = get_narrative_splitter()
    return splitter.split_text(text)
