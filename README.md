# StoryLens

### "Understand your story the way your readers do."

**StoryLens** is an advanced AI-powered narrative intelligence system built for modern fiction writers. Unlike standard grammar checkers, StoryLens acts as a **professional literary editor**, analyzing the deep architecture of your prose—pacing, emotional resonance, and structural rhythm—across English, Hindi, and Marathi.

---

## Why it's Special
Most AI writing tools feel robotic. StoryLens is different. It combines **precise NLP heuristics** with **state-of-the-art LLM reasoning** to provide feedback that actually helps a writer grow, not just "fix" text.

- **Deep Reasoning**: Instead of simple word-counting, it uses custom heuristics to detect repetitive sentence starts, monotonous pacing, and flat emotional arcs.
- **Native Multi-lingualism**: Built with a custom RAG (Retrieval-Augmented Generation) pipeline supporting English, Hindi, and Marathi. It doesn't just translate; it understands cultural and linguistic nuances.
- **Professional Editor Workflow**: Powered by **LangGraph**, the system orchestrates a sophisticated "Think-Write-Evaluate" cycle, ensuring every suggestion is high-quality and tone-consistent.
- **RAG-Powered Inspiration**: Connects your writing to a database of thousands of high-quality story segments (TinyStories & IITB Corpus) to suggest improvements based on proven narrative success.

---

## Technical Architecture

StoryLens is a full-stack AI system designed for scale and measurable reasoning:

- **Orchestration**: `LangChain` & `LangGraph` (Conditional state-based workflows).
- **Inference**: `Groq API` (Llama-3.3-70b-versatile) for lightning-fast reasoning.
- **Intelligence**: 
  - **Custom Heuristics Layer**: Python-based modules for pacing and repetition analysis.
  - **Feature Extraction**: SpaCy, TextBlob, and Transformers.
- **RAG System**:
  - **Embeddings**: `intfloat/multilingual-e5-base` (Optimized for cross-lingual retrieval).
  - **Vector Store**: `FAISS` (Localized high-speed retrieval).
- **UI**: `Streamlit` (A focused, writer-centric interface).

---

## Installation & Setup

### 1. Environment Preparation
```bash
# Create a dedicated environment
python -m venv storylens_env
source storylens_env/bin/activate  # Mac/Linux
storylens_env\Scripts\activate     # Windows

# Install core dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_key_here
```

### 3. Initialize the Vector Intelligence
```bash
# 1. Download high-quality datasets
python ingestion/download_datasets.py

# 2. Build the FAISS intelligence base
python ingestion/embedding_pipeline.py
```

### 4. Launch StoryLens
```bash
streamlit run app.py
```

---

## Project Structure
- `agents/`: Dedicated LLM experts for Rewriting, Feedback, and Summarization.
- `langgraph_flow/`: The "brain" of the system—orchestrating the conditional analysis workflow.
- `features/`: The "eyes" of the system—heuristic modules extracting raw narrative metrics.
- `rag/`: Vector search and retrieval-augmented generation logic.
- `ui/`: Clean, localized components for an immersive writing experience.

---

## Future Vision
- **Cross-Chapter Memory**: Tracking character arcs across an entire book.
- **Style Mimicry**: Training the RAG layer on a specific author's complete works.
- **Expanded Dialect Support**: Deep support for regional Indian languages and dialects.

---
*Created with passion for the art of storytelling.*

