# ====================================================
# FILE PURPOSE
# ====================================================
# Automatically downloads, lightly processes, and locally stores
# the datasets required for the RAG system.
# Targets TinyStories (English) and Hindi datasets.

import os
import json
from datasets import load_dataset
from src.utils.logger import get_logger

logger = get_logger(__name__)

def download_english():
    logger.info("Downloading English dataset (TinyStories)...")
    dataset = load_dataset("roneneldan/TinyStories", split="train[:1000]")
    
    out_dir = "data/raw_stories/english"
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = os.path.join(out_dir, "tinystories_1000.jsonl")
    with open(out_path, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps({"text": item["text"], "language": "english"}) + "\n")
    logger.info(f"Saved English dataset to {out_path}")

def download_hindi():
    logger.info("Downloading Hindi dataset (cfilt/iitb-english-hindi)...")
    # This is a very common and stable dataset
    try:
        dataset = load_dataset("cfilt/iitb-english-hindi", split="train[:1000]")
        
        out_dir = "data/raw_stories/hindi"
        os.makedirs(out_dir, exist_ok=True)
        
        out_path = os.path.join(out_dir, "hindi_iitb_1000.jsonl")
        with open(out_path, 'w', encoding='utf-8') as f:
            for item in dataset:
                # IITB items have a 'translation' dict with 'hi' key
                text = item["translation"]["hi"]
                if text:
                    f.write(json.dumps({"text": text, "language": "hindi"}) + "\n")
        logger.info(f"Saved Hindi dataset to {out_path}")
    except Exception as e:
        logger.error(f"Hindi dataset download failed: {e}")

if __name__ == "__main__":
    download_english()
    download_hindi()
