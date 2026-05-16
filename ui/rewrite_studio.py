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
    # Detect dominant language for UI labels
    lang = "english"
    if paragraphs_state:
        # Use language of the first paragraph
        lang = paragraphs_state[0].get("language", "english")

    all_labels = {
        "english": {"title": "Rewrite Studio", "orig": "Original Version", "suggested": "Improved Version", "empty": "No rewrites needed for this chapter."},
        "hindi": {"title": "लेखन सुधार स्टूडियो", "orig": "मूल पाठ", "suggested": "सुधरा हुआ संस्करण", "empty": "इस अध्याय के लिए किसी सुधार की आवश्यकता नहीं है।"},
        "marathi": {"title": "लेखन सुधार स्टुडिओ", "orig": "मूळ मजकूर", "suggested": "सुधारित आवृत्ती", "empty": "या प्रकरणासाठी कोणत्याही सुधारणेची आवश्यकता नाही."}
    }

    labels = all_labels.get(lang, all_labels["english"])
    
    labels = all_labels.get(lang, all_labels["english"])

    st.markdown(f"### {labels['title']}")
    
    rewritten_paragraphs = [p for p in paragraphs_state if p["rewritten_text"]]
    
    if not rewritten_paragraphs:
        st.info(labels["empty"])
        return
        
    for state in rewritten_paragraphs:
        para_label = {"english": "Paragraph", "hindi": "अनुच्छेद", "marathi": "परिच्छेद"}.get(lang, "Paragraph")
        what_label = {"english": "What changed?", "hindi": "क्या बदलाव हुए?", "marathi": "काय बदल झाले?"}.get(lang, "What changed?")
        
        st.markdown(f"#### {para_label} {state['paragraph_id'] + 1}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{labels['orig']}**")
            st.text_area("original", state["original_text"], height=200, disabled=True, label_visibility="collapsed", key=f"orig_{state['paragraph_id']}")
            
        with col2:
            st.markdown(f"**{labels['suggested']}**")
            st.text_area("rewrite", state["rewritten_text"], height=200, label_visibility="collapsed", key=f"rewr_{state['paragraph_id']}")
            
        # Explanation section
        st.markdown(f"**{what_label}**")
        st.write(state["rewrite_explanation"])
        st.markdown("---")

