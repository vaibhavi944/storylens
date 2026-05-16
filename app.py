# ====================================================
# FILE PURPOSE
# ====================================================
# Main entry point for the StoryLens Streamlit application.
# Organized into dedicated language sections (EN, HI, MR).

import streamlit as st
import os
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

from src.utils.formatting import split_into_paragraphs
from src.langgraph_flow.graph import process_paragraph

from src.ui.heatmap import render_heatmap
from src.ui.feedback_cards import render_feedback_cards
from src.ui.rewrite_studio import render_rewrite_studio
from src.ui.summary_report import render_summary_report

# Page Config
st.set_page_config(
    page_title="StoryLens",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Product-grade visual polish CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap');

    .stApp {
        background-color: #f5f4f0;
        font-family: 'Inter', sans-serif;
        color: #1c2b2b;
    }

    /* Main container width */
    .block-container {
        max-width: 880px;
        padding-top: 3rem;
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Source Serif 4', serif !important;
        color: #1c2b2b !important;
        font-weight: 600 !important;
    }
    
    h1 {
        font-size: 2.2rem !important;
        letter-spacing: -0.3px !important;
        margin-bottom: 0.2rem !important;
    }

    h4 {
        font-family: 'Inter', sans-serif !important;
        color: #6b7f7f !important;
        font-weight: 400 !important;
        font-size: 1rem !important;
        margin-top: 0 !important;
    }

    .stMarkdown p, .stMarkdown div {
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem;
        line-height: 1.75;
        color: #1c2b2b;
    }

    /* Radio button container */
    div[data-baseweb="radio"] {
        background-color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: 1px solid #dddad4;
    }
    
    div[data-baseweb="radio"] label {
        font-weight: 500 !important;
        color: #1c2b2b !important;
    }

    /* Selectbox styling */
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        border: 1px solid #dddad4 !important;
        border-radius: 8px !important;
    }

    /* Textarea styling */
    .stTextArea textarea {
        background-color: white !important;
        border: 1.5px solid #dddad4 !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.75 !important;
        padding: 1rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #2d6a6a !important;
        box-shadow: 0 0 0 4px rgba(45, 106, 106, 0.12) !important;
    }

    /* Main button styling */
    .stButton>button {
        background-color: #2d6a6a !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        height: 3.2rem !important;
        transition: all 0.2s ease !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #1f4f4f !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(45, 106, 106, 0.25) !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #2d6a6a !important;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 2px solid #dddad4 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #6b7f7f !important;
        background-color: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #2d6a6a !important;
        border-bottom: 2px solid #2d6a6a !important;
    }

    /* Download button */
    .stDownloadButton>button {
        background-color: #eef4f4 !important;
        color: #2d6a6a !important;
        border: 1.5px solid #2d6a6a !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }

    /* Alert boxes */
    .stAlert {
        border-radius: 10px !important;
        border: none !important;
    }
    
    /* Remove default left border on alerts */
    .stAlert > div {
        border-left: none !important;
    }
    
    .stCaption {
        color: #6b7f7f !important;
        font-size: 0.85rem !important;
    }
    </style>
""", unsafe_allow_html=True)

def run_analysis(story_input, lang_code, ui_labels, selected_genre):
    """
    Core analysis logic shared across pages.
    """
    if not story_input.strip():
        st.warning(ui_labels["warning_text"])
        return
        
    paragraphs = split_into_paragraphs(story_input)
    
    if not paragraphs:
        st.warning("Could not identify paragraphs.")
        return
        
    status_container = st.empty()
    status_container.info(ui_labels["info_analyzing"].format(n=len(paragraphs)))
    
    progress_bar = st.progress(0)
    
    results = []
    for i, para in enumerate(paragraphs):
        # Process via LangGraph
        state = process_paragraph(para, paragraph_id=i, genre=selected_genre)
        state["language"] = lang_code 
        results.append(state)
        progress_bar.progress((i + 1) / len(paragraphs))
        
    status_container.success(ui_labels["success"])
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(ui_labels["tabs"])
    
    with tab1:
        render_heatmap(results)
    with tab2:
        render_feedback_cards(results)
    with tab3:
        render_rewrite_studio(results)
    with tab4:
        render_summary_report(results)
        # Add Download Button to Summary
        report_text = f"StoryLens Analysis Report\nGenre: {selected_genre}\nLanguage: {lang_code}\n\n"
        for r in results:
            report_text += f"Para {r['paragraph_id']+1} ({r['label']}): {r['original_text']}\n\n"
        st.download_button("Download Full Report", report_text, file_name="storylens_report.txt")

def main():
    st.markdown("<h1>StoryLens</h1>", unsafe_allow_html=True)
    st.markdown("#### *Understand your story the way your readers do*")
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Check for API Key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        st.error("GROQ_API_KEY not found in .env file.")

    # Three separate pages/tabs for languages as requested
    selected_lang = st.radio(
        "Select Language / भाषा चुनें", 
        ["English", "Hindi / हिंदी", "Marathi / मराठी"],
        horizontal=True
    )


    if selected_lang == "English":
        lang_key = "english"
        ui_labels = {
            "title": "English Story Analysis",
            "desc": "An AI-assisted narrative intelligence system that identifies pacing issues and suggests improvements.",
            "genre": "Genre Focus",
            "genres": ["General", "Romance", "Thriller", "Fantasy", "Drama"],
            "paste": "Paste your English chapter here:",
            "placeholder": "Once upon a time...",
            "button": "Analyze Chapter",
            "warning_text": "Please enter some text to analyze.",
            "info_analyzing": "Analyzing {n} paragraphs. Please wait...",
            "success": "Analysis Complete!",
            "tabs": ["Story Overview", "Feedback Cards", "Rewrite Studio", "Summary Report"],
            "about": "About StoryLens"
        }
    elif selected_lang == "Hindi / हिंदी":
        lang_key = "hindi"
        ui_labels = {
            "title": "हिंदी कहानी विश्लेषण",
            "desc": "एक एआई-आधारित कहानी विश्लेषण प्रणाली जो बिना किसी तकनीकी शब्दावली के लेखन में सुधार के सुझाव देती है।",
            "genre": "कहानी की शैली (Genre)",
            "genres": ["सामान्य (General)", "रोमांस (Romance)", "थ्रिलर (Thriller)", "कल्पना (Fantasy)", "नाटक (Drama)"],
            "paste": "अपनी हिंदी कहानी यहाँ पेस्ट करें:",
            "placeholder": "एक समय की बात है...",
            "button": "अध्याय का विश्लेषण करें",
            "warning_text": "कृपया विश्लेषण के लिए कुछ टेक्स्ट दर्ज करें।",
            "info_analyzing": "{n} अनुच्छेदों का विश्लेषण किया जा रहा है। कृपया प्रतीक्षा करें...",
            "success": "विश्लेषण पूर्ण!",
            "tabs": ["कहानी का प्रवाह (Overview)", "सुझाव कार्ड", "सुधार स्टूडियो", "सारांश रिपोर्ट"],
            "about": "स्टोरीलेंस के बारे में"
        }
    else: # Marathi
        lang_key = "marathi"
        ui_labels = {
            "title": "मराठी कथा विश्लेषण",
            "desc": "एक AI-आधारित कथा विश्लेषण प्रणाली जी तांत्रिक शब्दावलीशिवाय लेखनात सुधारणा सुचवते.",
            "genre": "कथेची शैली (Genre)",
            "genres": ["सामान्य (General)", "रोमान्स (Romance)", "थ्रिलर (Thriller)", "काल्पनिक (Fantasy)", "नाटक (Drama)"],
            "paste": "तुमची मराठी कथा येथे पेस्ट करा:",
            "placeholder": "एकदा एक...",
            "button": "प्रकरणाचे विश्लेषण करा",
            "warning_text": "कृपया विश्लेषणासाठी काही मजकूर प्रविष्ट करा.",
            "info_analyzing": "{n} परिच्छेदांचे विश्लेषण होत आहे. कृपया प्रतीक्षा करा...",
            "success": "विश्लेषण पूर्ण!",
            "tabs": ["कथेचा ओघ (Overview)", "अभिप्राय कार्ड", "सुधारणा स्टुडिओ", "सारांश अहवाल"],
            "about": "स्टोरीलेंस बद्दल"
        }

    st.subheader(ui_labels["title"])
    st.markdown(f"*{ui_labels['desc']}*")
    
    # Genre Focus Selector
    selected_genre = st.selectbox(
        ui_labels["genre"], 
        ui_labels["genres"],
        key=f"genre_{lang_key}"
    )

    story_input = st.text_area(
        ui_labels["paste"], 
        height=300, 
        placeholder=ui_labels["placeholder"],
        key=f"input_{lang_key}"
    )
    
    if st.button(ui_labels["button"], use_container_width=True, key=f"btn_{lang_key}"):
        run_analysis(story_input, lang_key, ui_labels, selected_genre)

    # Footer Caption
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center; color: #9aabab; font-size: 0.8rem; font-family: Inter, sans-serif;'>"
        "StoryLens · AI-assisted narrative intelligence"
        "</div>", 
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
