# ====================================================
# FILE PURPOSE
# ====================================================
# Renders a final summary report of the chapter's overall
# strengths and weaknesses.

import streamlit as st
from src.agents.summary_agent import generate_overall_advice

def render_summary_report(paragraphs_state: list[dict]):
    """
    Compiles overall metrics into a simple report.
    """
    lang = "english"
    if paragraphs_state:
        lang = paragraphs_state[0].get("language", "english")

    all_labels = {
        "english": {
            "title": "Chapter Summary", "total": "Total Paragraphs", "strong": "Strong Sections",
            "polish": "Areas to Polish", "advice": "Overall Advice"
        },
        "hindi": {
            "title": "अध्याय का सारांश", "total": "कुल अनुच्छेद", "strong": "मजबूत हिस्से",
            "polish": "सुधार के क्षेत्र", "advice": "कुल मिलाकर सलाह"
        },
        "marathi": {
            "title": "प्रकरणाचा सारांश", "total": "एकूण परिच्छेद", "strong": "मजबूत भाग",
            "polish": "सुधारणेसाठी जागा", "advice": "एकूण सल्ला"
        }
    }

    labels = all_labels.get(lang, all_labels["english"])

    st.markdown(f"### {labels['title']}")
    
    total = len(paragraphs_state)
    if total == 0:
        return
        
    strong_count = sum(1 for p in paragraphs_state if p["label"] == "strong")
    weak_count = sum(1 for p in paragraphs_state if p["label"] == "weak")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(labels["total"], total)
    col2.metric(labels["strong"], strong_count)
    col3.metric(labels["polish"], weak_count)
    
    st.markdown(f"#### {labels['advice']}")
    
    # Generate dynamic, context-aware advice using LLM
    with st.spinner("Generating personalized advice..."):
        advice = generate_overall_advice(paragraphs_state, lang)
        st.write(advice)
