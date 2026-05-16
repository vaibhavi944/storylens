# ====================================================
# FILE PURPOSE
# ====================================================
# Renders a final summary report of the chapter's overall
# strengths and weaknesses.

import streamlit as st

def render_summary_report(paragraphs_state: list[dict]):
    """
    Compiles overall metrics into a simple report.
    """
    st.markdown("### Chapter Summary")
    
    total = len(paragraphs_state)
    if total == 0:
        return
        
    strong_count = sum(1 for p in paragraphs_state if p["label"] == "strong")
    weak_count = sum(1 for p in paragraphs_state if p["label"] == "weak")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Paragraphs", total)
    col2.metric("Strong Sections", strong_count)
    col3.metric("Areas to Polish", weak_count)
    
    st.markdown("#### Overall Advice")
    if strong_count / total > 0.7:
        st.write("Excellent pacing and engagement! Your chapter reads beautifully.")
    elif weak_count / total > 0.4:
        st.write("Consider focusing on varying your sentence lengths and ensuring emotional beats hit harder.")
    else:
        st.write("A solid foundation. Polishing a few transitions will make this shine.")
