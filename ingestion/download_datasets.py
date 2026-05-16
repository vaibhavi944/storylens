# ====================================================
# FILE PURPOSE
# ====================================================
# Automatically downloads, lightly processes, and locally stores
# the datasets required for the RAG system.
# Targets TinyStories (English) and hindi_discourse (Hindi).

import os
import json
from datasets import load_dataset
from utils.logger import get_logger

logger = get_logger(__name__)

def download_english():
    logger.info("Downloading English dataset (TinyStories)...")
    dataset = load_dataset("roneneldan/TinyStories", split="train[:500]")
    
    out_dir = "data/raw_stories/english"
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = os.path.join(out_dir, "tinystories_500.jsonl")
    with open(out_path, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps({"text": item["text"], "language": "english"}) + "\n")
    logger.info(f"Saved English dataset to {out_path}")

def download_hindi():
    logger.info("Downloading Hindi dataset (hindi_discourse)...")
    # Take a small subset for demonstration purposes
    dataset = load_dataset("midas/hindi_discourse", split="train[:500]")
    
    out_dir = "data/raw_stories/hindi"
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = os.path.join(out_dir, "hindi_discourse_500.jsonl")
    with open(out_path, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps({"text": item["text"], "language": "hindi"}) + "\n")
    logger.info(f"Saved Hindi dataset to {out_path}")

if __name__ == "__main__":
    download_english()
    try:
        download_hindi()
    except Exception as e:
        logger.error(f"Hindi dataset download failed (it may be gated or unavailable): {e}")
