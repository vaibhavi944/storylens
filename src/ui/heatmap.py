# ====================================================
# FILE PURPOSE
# ====================================================
# Renders the full chapter with color-coded highlighting
# based on the weakness score (Green, Yellow, Red).

import streamlit as st
from src.utils.scoring_utils import label_to_color

def render_heatmap(paragraphs_state: list[dict]):
    """
    Renders the story flow overview.
    Each paragraph is highlighted based on its label.
    """
    lang = "english"
    if paragraphs_state:
        lang = paragraphs_state[0].get("language", "english")

    all_labels = {
        "english": {"title": "Story Overview", "cap": "Click on a paragraph to view detailed feedback below.", "s": "Strong", "m": "Moderate", "w": "Weak", "s_desc": "Readers stay hooked.", "m_desc": "Attention may drift.", "w_desc": "Risk of losing reader."},
        "hindi": {"title": "कहानी का प्रवाह (Overview)", "cap": "विस्तृत प्रतिक्रिया देखने के लिए किसी अनुच्छेद पर क्लिक करें।", "s": "मजबूत", "m": "सामान्य", "w": "कमजोर", "s_desc": "पाठक कहानी से जुड़े रहते हैं।", "m_desc": "ध्यान भटक सकता है।", "w_desc": "पाठक को खोने का जोखिम।"},
        "marathi": {"title": "कथेचा ओघ (Overview)", "cap": "तपशीलवार अभिप्राय पाहण्यासाठी परिच्छेदावर क्लिक करा.", "s": "मजबूत", "m": "मध्यम", "w": "कमकुवत", "s_desc": "वाचक खिळून राहतात.", "m_desc": "लक्ष विचलित होऊ शकते.", "w_desc": "वाचक गमावण्याचा धोका."}
    }
    
    labels = all_labels.get(lang, all_labels["english"])

    st.markdown(f"### {labels['title']}")
    st.caption(labels["cap"])
    
    html_blocks = []
    
    for state in paragraphs_state:
        color = label_to_color(state["label"])
        
        # Soft pastel colors for readability
        bg_color = {
            "green": "#e6f4ea",
            "yellow": "#fff8e1",
            "red": "#fce8e6",
            "grey": "#f1f3f4"
        }.get(color, "#f1f3f4")
        
        border_color = {
            "green": "#ceead6",
            "yellow": "#ffefc0",
            "red": "#fad2cf",
            "grey": "#dadce0"
        }.get(color, "#dadce0")
        
        # Build block as single line to avoid Streamlit markdown break issues
        block = f"<div style='background-color: {bg_color}; border-left: 4px solid {border_color}; padding: 12px; margin-bottom: 12px; border-radius: 4px; color: #2c3e50; line-height: 1.6; font-size: 1.05em;'>{state['original_text']}</div>"
        html_blocks.append(block)
        
    full_html = "".join(html_blocks)
    st.markdown(full_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Legend Layout Fix - clean horizontal row with equal spacing
    col1, col2, col3 = st.columns(3)
    
    # Using CSS circles instead of emojis to comply with "No emojis" while keeping "Color circles"
    circle_style = "display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:8px;"
    
    col1.markdown(
        f"<div style='display:flex; align-items:center; font-size:0.9rem; color:#6b7f7f;'>"
        f"<div style='{circle_style} background-color:#e6f4ea; border:1px solid #ceead6;'></div>"
        f"<strong>{labels['s']}</strong>: {labels['s_desc']}</div>", 
        unsafe_allow_html=True
    )
    col2.markdown(
        f"<div style='display:flex; align-items:center; font-size:0.9rem; color:#6b7f7f;'>"
        f"<div style='{circle_style} background-color:#fff8e1; border:1px solid #ffefc0;'></div>"
        f"<strong>{labels['m']}</strong>: {labels['m_desc']}</div>", 
        unsafe_allow_html=True
    )
    col3.markdown(
        f"<div style='display:flex; align-items:center; font-size:0.9rem; color:#6b7f7f;'>"
        f"<div style='{circle_style} background-color:#fce8e6; border:1px solid #fad2cf;'></div>"
        f"<strong>{labels['w']}</strong>: {labels['w_desc']}</div>", 
        unsafe_allow_html=True
    )
