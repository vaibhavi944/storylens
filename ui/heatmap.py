# ====================================================
# FILE PURPOSE
# ====================================================
# Renders the full chapter with color-coded highlighting
# based on the weakness score (Green, Yellow, Red).

import streamlit as st
from utils.scoring_utils import label_to_color

def render_heatmap(paragraphs_state: list[dict]):
    """
    Renders the story heatmap.
    Each paragraph is highlighted based on its label.
    """
    st.markdown("### Story Heatmap")
    st.caption("Click on a paragraph to view detailed feedback below.")
    
    html_content = "<div style='line-height: 1.6; font-size: 1.1em;'>"
    
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
        
        html_content += f"""
        <div style='background-color: {bg_color}; border-left: 4px solid {border_color}; padding: 10px; margin-bottom: 10px; border-radius: 4px;'>
            {state["original_text"]}
        </div>
        """
        
    html_content += "</div>"
    st.markdown(html_content, unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.markdown("🟢 **Strong**: Readers stay hooked.")
    col2.markdown("🟡 **Moderate**: Attention may drift.")
    col3.markdown("🔴 **Weak**: Risk of losing reader.")
