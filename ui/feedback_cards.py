# ====================================================
# FILE PURPOSE
# ====================================================
# Renders writer-friendly feedback cards for weak paragraphs.

import streamlit as st

def render_feedback_cards(paragraphs_state: list[dict]):
    """
    Displays actionable feedback for paragraphs that need improvement.
    """
    st.markdown("### Feedback & Suggestions")
    
    needs_work = [p for p in paragraphs_state if p["label"] != "strong"]
    
    if not needs_work:
        st.success("Great job! Your chapter flows well and maintains strong reader engagement.")
        return
        
    for state in needs_work:
        with st.expander(f"Paragraph {state['paragraph_id'] + 1}: {state['feedback_title']}"):
            st.markdown(f"**Issue:** {state['feedback_explanation']}")
            st.markdown(f"**Suggestion:** {state['feedback_suggestion']}")
            
            st.markdown("**Original Text:**")
            st.info(state["original_text"])
            
            if state["rewritten_text"]:
                st.markdown("---")
                st.markdown("**Consider this approach:**")
                st.success(state["rewritten_text"])
                st.caption(f"**Why this works:** {state['rewrite_explanation']}")
