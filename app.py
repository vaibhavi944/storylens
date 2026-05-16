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

# Custom CSS for aesthetic styling
st.markdown("""
    <style>
    .stApp {
        background-color: #faf9f6;
        color: #2c3e50;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #2c3e50 !important;
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
    st.title("📖 StoryLens")
    
    # Sidebar Setup
    st.sidebar.header("Settings / सेटिंग्स")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        st.sidebar.error("⚠️ GROQ_API_KEY not found.")
    else:
        st.sidebar.success("✅ Connected")

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
            "genres": ["सामान्य (General)", "रोमान्स (Romance)", "थ्रिलर (Thriller)", "काल्पनिक (Fantasy)", "नाटक (Drama)"],
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
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**{ui_labels['about']}**")
    
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


if __name__ == "__main__":
    main()
