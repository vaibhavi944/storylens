# StoryLens

"Understand your story the way your readers do"

StoryLens is an AI-assisted multilingual narrative intelligence system for fiction writers inspired by platforms like Pratilipi. It uses advanced RAG workflows and NLP heuristics to identify narrative weaknesses, suggest improvements, and fetch similar strong examples, all while preserving the author's tone and avoiding technical jargon.

## Architecture

![Architecture Diagram Placeholder](https://via.placeholder.com/800x400.png?text=StoryLens+Architecture)

* Frontend: Streamlit
* Backend: Python
* LLM Orchestration: LangChain & LangGraph
* LLM Provider: Groq API (llama-3.3-70b-versatile)
* Embeddings: intfloat/multilingual-e5-base
* Vector Store: FAISS
* Processing: SpaCy, TextBlob, Transformers

====================================================
## ENVIRONMENT SETUP REQUIREMENTS
====================================================

Before building the project, please set up an isolated virtual environment. The project heavily depends on specific versions of ML/NLP libraries which might conflict with global installations.

### 1. Create a dedicated Python virtual environment

**Environment name:** `storylens_env`

#### Windows:
```bash
python -m venv storylens_env
```

#### Mac/Linux:
```bash
python3 -m venv storylens_env
```

### 2. Activate the environment

#### Windows:
```bash
storylens_env\Scripts\activate
```

#### Mac/Linux:
```bash
source storylens_env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```
Edit `.env` and add your Groq API key:
`GROQ_API_KEY=your_groq_api_key_here`

### 5. VS Code Configuration (Optional but Recommended)
- Ensure the Python extension is installed.
- Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`) and select `Python: Select Interpreter`.
- Choose the interpreter located inside `storylens_env`.

====================================================
## RUN COMMAND REQUIREMENTS
====================================================

To run the full pipeline, execute the following commands in order:

### 1. Download Datasets
Downloads English (TinyStories) and Hindi (hindi_discourse) sample datasets for RAG.
```bash
python ingestion/download_datasets.py
```

### 2. Run Embedding Pipeline
Processes the raw downloaded stories, applies chunking, generates metadata, and stores vectors in FAISS.
```bash
python ingestion/embedding_pipeline.py
```

### 3. Start Streamlit App
Launches the interactive UI.
```bash
streamlit run app.py
```

## Features
- **Narrative Weakness Detection**: Detects issues in pacing, emotion, and repetitive dialogue ratios using pure heuristics and NLP before relying on LLMs.
- **Multilingual Support**: Supports English, Hindi, and Marathi narratives.
- **Tone Preservation**: Rewrites suggestions adapt to your specific narrative voice.
- **Reader-Centric Explanations**: No RAG/Cosine similarity jargon; pure, writer-friendly feedback.

## Folder Structure
- `app.py`: Main Streamlit application.
- `ingestion/`: Scripts for downloading datasets, preprocessing, and building the FAISS vector database.
- `rag/`: Vector database and retrieval definitions.
- `features/`: Pure Python modules extracting narrative metrics from text.
- `scoring/`: Weakness estimation based on narrative heuristics.
- `prompts/`: LLM instructional prompts.
- `agents/`: Core LLM interaction modules.
- `langgraph_flow/`: Routing and conditional pipelines for analyzing and rewriting content.
- `ui/`: Subcomponents for the Streamlit UI.
- `utils/`: Helpers, formatting, and logging.
- `data/`: Storage for datasets.

## Future Improvements
- Deeper narrative arc analysis.
- Multi-chapter context tracking.
- More robust support for low-resource languages.
