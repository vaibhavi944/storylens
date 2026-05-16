# ====================================================
# FILE PURPOSE
# ====================================================
# Renders writer-friendly feedback cards for weak paragraphs.

import streamlit as st

def render_feedback_cards(paragraphs_state: list[dict]):
    """
    Displays actionable feedback for paragraphs that need improvement.
    """
    lang = "english"
    if paragraphs_state:
        lang = paragraphs_state[0].get("language", "english")

    all_labels = {
        "english": {
            "title": "Feedback & Suggestions",
            "success": "Great job! Your chapter flows well and maintains strong reader engagement.",
            "issue": "Issue", "suggestion": "Suggestion", "orig": "Original Text",
            "approach": "Consider this approach", "why": "Why this works", "para": "Paragraph"
        },
        "hindi": {
            "title": "सुझाव और प्रतिक्रिया",
            "success": "बहुत बढ़िया! आपका अध्याय अच्छी तरह से प्रवाहित होता है और पाठकों को जोड़े रखता है।",
            "issue": "समस्या", "suggestion": "सुझाव", "orig": "मूल पाठ",
            "approach": "इस दृष्टिकोण पर विचार करें", "why": "यह क्यों काम करता है", "para": "अनुच्छेद"
        },
        "marathi": {
            "title": "अभिप्राय आणि सूचना",
            "success": "छान! तुमचे प्रकरण प्रवाही आहे आणि वाचकांना खिळवून ठेवते.",
            "issue": "समस्या", "suggestion": "सूचना", "orig": "मूळ मजकूर",
            "approach": "या पर्यायाचा विचार करा", "why": "हे का प्रभावी आहे", "para": "परिच्छेद"
        }
    }
    
    labels = all_labels.get(lang, all_labels["english"])

    st.markdown(f"### {labels['title']}")
    
    needs_work = [p for p in paragraphs_state if p["label"] != "strong"]
    
    if not needs_work:
        st.success(labels["success"])
        return
        
    for state in needs_work:
        with st.expander(f"{labels['para']} {state['paragraph_id'] + 1}: {state['feedback_title']}"):
            st.markdown(f"**{labels['issue']}:** {state['feedback_explanation']}")
            st.markdown(f"**{labels['suggestion']}:** {state['feedback_suggestion']}")
            
            st.markdown(f"**{labels['orig']}:**")
            st.info(state["original_text"])
            
            if state["rewritten_text"]:
                st.markdown("---")
                st.markdown(f"**{labels['approach']}:**")
                st.success(state["rewritten_text"])
                st.caption(f"**{labels['why']}:** {state['rewrite_explanation']}")
