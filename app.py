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
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Upgraded CSS for product-grade visual polish
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .stApp {
        background-color: #f7f5f0;
        font-family: 'Inter', sans-serif;
    }

    /* Main container width */
    .block-container {
        max-width: 860px;
        padding-top: 2rem;
    }

    /* Typography */
    h1 {
        color: #1a2e35 !important;
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }
    h4 {
        color: #5a7a7a !important;
        font-weight: 400 !important;
        font-size: 1.05rem !important;
    }

    /* Radio button container */
    div[data-baseweb="radio"] {
        background-color: white;
        border-radius: 12px;
        padding: 0.6rem 1rem;
        border: 1px solid #e0ddd6;
    }

    /* Selectbox styling */
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        border: 1px solid #d4cfc7 !important;
        border-radius: 10px !important;
    }

    /* Textarea styling */
    .stTextArea textarea {
        background-color: white !important;
        border: 1.5px solid #d4cfc7 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        line-height: 1.7 !important;
    }
    .stTextArea textarea:focus {
        border-color: #008080 !important;
        box-shadow: 0 0 0 2px rgba(0, 128, 128, 0.1) !important;
    }

    /* Main button styling */
    .stButton>button {
        background-color: #006d6d !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        height: 3rem !important;
        transition: all 0.2s ease !important;
        border: none !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 109, 109, 0.2) !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #008080 !important;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 2px solid #e0ddd6 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #5a7a7a !important;
    }
    .stTabs [aria-selected="true"] {
        color: #006d6d !important;
        border-bottom: 2px solid #006d6d !important;
    }

    /* Download button */
    .stDownloadButton>button {
        background-color: #f0f7f7 !important;
        color: #008080 !important;
        border: 1px solid #008080 !important;
        border-radius: 10px !important;
    }

    /* Alert boxes */
    .stAlert {
        border-radius: 10px !important;
        border: none !important;
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
    st.markdown("<h1>📖 StoryLens</h1>", unsafe_allow_html=True)
    st.markdown("#### *Understand your story the way your readers do*")
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Check for API Key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        st.error("⚠️ GROQ_API_KEY not found in .env file.")

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
            "tabs": ["कहानी का प्रवाह", "सुझाव कार्ड", "सुधार स्टूडियो", "सारांश रिपोर्ट"],
            "about": "स्टोरीलेंस के बारे में"
        }
    else: # Marathi
        lang_key = "marathi"
        ui_labels = {
            "title": "मराठी कथा विश्लेषण",
            "desc": "एक AI-आधारित कथा विश्लेषण प्रणाली जी तांत्रिक शब्दावलीशिवाय लेखनात सुधारणा सुचवते.",
            "genre": "कथेची शैली (Genre)",
            "genres": ["सामान्य (General)", "रोमांस (Romance)", "थ्रिलर (Thriller)", "काल्पनिक (Fantasy)", "नाटक (Drama)"],
            "paste": "तुमची मराठी कथा येथे पेस्ट करा:",
            "placeholder": "एकदा एक...",
            "button": "प्रकरणाचे विश्लेषण करा",
            "warning_text": "कृपया विश्लेषणासाठी काही मजकूर प्रविष्ट करा.",
            "info_analyzing": "{n} परिच्छेदांचे विश्लेषण होत आहे. कृपया प्रतीक्षा करा...",
            "success": "विश्लेषण पूर्ण!",
            "tabs": ["कथेचा ओघ", "अभिप्राय कार्ड", "सुधारणा स्टुडिओ", "सारांश अहवाल"],
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
        "<div style='text-align: center; color: #9aabab; font-size: 0.82rem;'>"
        "StoryLens · AI-assisted narrative intelligence · Built for Pratilipi writers"
        "</div>", 
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
