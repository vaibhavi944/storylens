# StoryLens

Understand your story the way your readers do.

StoryLens is an AI-powered narrative intelligence system for fiction writers. It analyzes the deep structure of prose — pacing, emotional arc, and structural rhythm — and suggests specific, reasoned improvements. It works natively across English, Hindi, and Marathi.

---

## Why StoryLens

- **Deep Heuristics**: Detects repetitive sentence starts, monotonous pacing, and flat emotional arcs using custom NLP modules, not simple word counting.
- **Native Multilingual Support**: A custom RAG pipeline built for English, Hindi, and Marathi that understands linguistic and cultural context, not just translation.
- **Stateful Workflow**: Powered by LangGraph, the system runs a conditional think-analyze-rewrite cycle ensuring tone-consistent, high-quality suggestions.
- **RAG-Powered Feedback**: Retrieves relevant segments from a curated story database to ground every suggestion in proven narrative patterns.

---

## Architecture

| Category | Stack |
|----------|-------|
| Orchestration | LangChain, LangGraph |
| Inference | Groq API (Llama-3.3-70b-versatile) |
| Heuristics | Custom Python modules, spaCy, TextBlob |
| Embeddings | intfloat/multilingual-e5-base |
| Vector Store | FAISS |
| Interface | Streamlit |

---

## Installation

**1. Environment setup**

```bash
python -m venv storylens_env
source storylens_env/bin/activate
storylens_env\Scripts\activate     # Windows only

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**2. Configuration**

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_key_here
```

**3. Build the vector database**

```bash
python ingestion/download_datasets.py
python ingestion/embedding_pipeline.py
```

**4. Run**

```bash
streamlit run app.py
```

---

## Project Structure
storylens/
├── src/
│   ├── agents/          # LLM rewrite and feedback agents
│   ├── features/        # Narrative heuristic extractors
│   ├── ingestion/       # Dataset download and embedding pipeline
│   ├── langgraph_flow/  # Conditional analysis workflow
│   ├── prompts/         # System and editorial prompts
│   ├── rag/             # Vector retrieval logic
│   ├── scoring/         # Paragraph weakness scoring
│   ├── ui/              # Modular Streamlit components
│   └── utils/           # Shared utilities
├── tests/               # Validation and sample inputs
├── .streamlit/          # App configuration
├── app.py               # Entry point
├── README.md
└── requirements.txt

---

## Roadmap

- Cross-chapter memory to track character and plot arcs across a full manuscript
- Style adaptation by training the RAG layer on a specific author's body of work
- Expanded support for regional Indian languages and mixed-language prose