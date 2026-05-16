# ====================================================
# FILE PURPOSE
# ====================================================
# Renders a side-by-side view for comparing original text
# with rewrite suggestions.

import streamlit as st

def render_rewrite_studio(paragraphs_state: list[dict]):
    """
    A dedicated studio view for selecting and applying rewrites.
    """
    st.markdown("### Rewrite Studio")
    
    rewritten_paragraphs = [p for p in paragraphs_state if p["rewritten_text"]]
    
    if not rewritten_paragraphs:
        st.info("No rewrites needed for this chapter.")
        return
        
    for state in rewritten_paragraphs:
        st.markdown(f"#### Edit Paragraph {state['paragraph_id'] + 1}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Original**")
            st.text_area("original", state["original_text"], height=150, disabled=True, label_visibility="collapsed", key=f"orig_{state['paragraph_id']}")
            
        with col2:
            st.markdown("**Suggested Rewrite**")
            st.text_area("rewrite", state["rewritten_text"], height=150, label_visibility="collapsed", key=f"rewr_{state['paragraph_id']}")
            
        st.markdown("---")
