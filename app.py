# ====================================================
# FILE PURPOSE
# ====================================================
# Main entry point for the StoryLens Streamlit application.
# Orchestrates input handling, graph execution, and UI rendering.

import streamlit as st
import os
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

from utils.formatting import split_into_paragraphs
from langgraph_flow.graph import process_paragraph

from ui.heatmap import render_heatmap
from ui.feedback_cards import render_feedback_cards
from ui.rewrite_studio import render_rewrite_studio
from ui.summary_report import render_summary_report

# Page Config
st.set_page_config(
    page_title="StoryLens",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetic styling (Warm, writer-friendly)
st.markdown("""
    <style>
    .stApp {
        background-color: #faf9f6;
    }
    h1, h2, h3 {
        font-family: 'Inter', 'Lato', sans-serif;
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #008080;
        color: white;
        border-radius: 6px;
    }
    .stTextArea>div>div>textarea {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("📖 StoryLens")
    st.markdown("#### *Understand your story the way your readers do*")
    
    st.sidebar.header("Settings")
    
    # Check for API Key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        st.sidebar.error("⚠️ GROQ_API_KEY not found in .env file. The application will run, but rewrites and metadata features will fall back to defaults or fail.")
    else:
        st.sidebar.success("✅ Groq API Connected")
        
    language = st.sidebar.selectbox("Language", ["Auto-detect", "English", "Hindi", "Marathi"])
    genre = st.sidebar.selectbox("Genre Focus", ["General", "Romance", "Thriller", "Fantasy", "Drama"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**About StoryLens**")
    st.sidebar.caption("An AI-assisted narrative intelligence system that identifies pacing issues and suggests improvements without technical jargon.")

    st.markdown("### Paste your chapter here:")
    story_input = st.text_area("Story Input", height=300, label_visibility="collapsed", placeholder="Once upon a time...")
    
    if st.button("Analyze Chapter", use_container_width=True):
        if not story_input.strip():
            st.warning("Please enter some text to analyze.")
            return
            
        paragraphs = split_into_paragraphs(story_input)
        
        if not paragraphs:
            st.warning("Could not identify paragraphs. Please format your text properly.")
            return
            
        st.info(f"Analyzing {len(paragraphs)} paragraphs. Please wait...")
        
        progress_bar = st.progress(0)
        
        results = []
        for i, para in enumerate(paragraphs):
            # Update status message
            status_text = "Reading your chapter..."
            if i > len(paragraphs) * 0.3:
                status_text = "Understanding emotional flow..."
            if i > len(paragraphs) * 0.6:
                status_text = "Finding similar successful scenes..."
            if i > len(paragraphs) * 0.8:
                status_text = "Preparing rewrite suggestions..."
                
            st.session_state["status_message"] = status_text
            
            # Process via LangGraph
            state = process_paragraph(para, paragraph_id=i)
            results.append(state)
            
            progress_bar.progress((i + 1) / len(paragraphs))
            
        st.success("Analysis Complete!")
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["Story Heatmap", "Feedback Cards", "Rewrite Studio", "Summary Report"])
        
        with tab1:
            render_heatmap(results)
            
        with tab2:
            render_feedback_cards(results)
            
        with tab3:
            render_rewrite_studio(results)
            
        with tab4:
            render_summary_report(results)

if __name__ == "__main__":
    main()
