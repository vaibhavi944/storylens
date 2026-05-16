# ====================================================
# FILE PURPOSE
# ====================================================
# Builds the LangGraph workflow for processing a single paragraph.
# Orchestrates feature extraction, scoring, rewriting, and evaluation.

from langgraph.graph import StateGraph, END
from src.langgraph_flow.state import ParagraphState
from src.features.narrative_metrics import extract_metrics
from src.scoring.weakness_scorer import score_paragraph
from src.scoring.plain_english_feedback import get_feedback_for_issue
from src.agents.rewrite_agent import generate_rewrite
from src.agents.evaluation_agent import evaluate_rewrite

def extract_features_node(state: ParagraphState) -> ParagraphState:
    metrics = extract_metrics(state["original_text"], state["paragraph_id"])
    scoring = score_paragraph(metrics)
    
    state["metrics"] = metrics
    state["score"] = scoring["score"]
    state["label"] = scoring["label"]
    state["primary_issue"] = scoring["primary_issue"]
    state["language"] = metrics["language"]
    
    return state

from src.agents.feedback_agent import generate_specific_feedback

def provide_feedback_node(state: ParagraphState) -> ParagraphState:
    if state["label"] != "strong" and state["primary_issue"]:
        # Get the generic title from our mapping
        generic_feedback = get_feedback_for_issue(state["primary_issue"], state["metrics"])
        state["feedback_title"] = generic_feedback["title"]
        
        # Call the LLM to get SPECIFIC explanation and suggestion
        specific_feedback = generate_specific_feedback(
            text=state["original_text"],
            language=state["language"],
            metrics=state["metrics"],
            weakness=state["primary_issue"]
        )
        
        # We store the specific feedback as the explanation
        state["feedback_explanation"] = specific_feedback
        state["feedback_suggestion"] = generic_feedback["suggestion"]
    return state


def rewrite_node(state: ParagraphState) -> ParagraphState:
    if state["rewrite_attempts"] >= 2:
        return state
        
    result = generate_rewrite(
        original_text=state["original_text"],
        language=state["language"],
        weakness=state["primary_issue"],
        explanation=state["feedback_explanation"],
        genre=state.get("genre", "General")
    )
    
    state["rewritten_text"] = result["rewrite"]
    state["rewrite_explanation"] = result["explanation"]
    state["rewrite_attempts"] += 1
    
    return state


def evaluate_node(state: ParagraphState) -> ParagraphState:
    if not state["rewritten_text"]:
        state["passed_evaluation"] = False
        return state
        
    passed = evaluate_rewrite(
        original_text=state["original_text"],
        rewritten_text=state["rewritten_text"],
        weakness=state["primary_issue"]
    )
    
    state["passed_evaluation"] = passed
    return state

def route_after_feature_extraction(state: ParagraphState) -> str:
    # If the paragraph is strong, skip rewriting
    if state["label"] == "strong":
        return END
    return "provide_feedback"

def route_after_evaluation(state: ParagraphState) -> str:
    if state["passed_evaluation"]:
        return END
    if state["rewrite_attempts"] >= 2:
        return END
    return "rewrite"

def build_paragraph_graph():
    workflow = StateGraph(ParagraphState)
    
    workflow.add_node("extract_features", extract_features_node)
    workflow.add_node("provide_feedback", provide_feedback_node)
    workflow.add_node("rewrite", rewrite_node)
    workflow.add_node("evaluate", evaluate_node)
    
    workflow.set_entry_point("extract_features")
    
    workflow.add_conditional_edges(
        "extract_features",
        route_after_feature_extraction,
        {END: END, "provide_feedback": "provide_feedback"}
    )
    
    workflow.add_edge("provide_feedback", "rewrite")
    workflow.add_edge("rewrite", "evaluate")
    
    workflow.add_conditional_edges(
        "evaluate",
        route_after_evaluation,
        {END: END, "rewrite": "rewrite"}
    )
    
    return workflow.compile()

def process_paragraph(text: str, paragraph_id: int = 0, genre: str = "General") -> ParagraphState:
    """
    Helper function to run the graph on a single paragraph.
    """
    graph = build_paragraph_graph()
    initial_state = ParagraphState(
        paragraph_id=paragraph_id,
        original_text=text,
        language="unknown",
        genre=genre,
        metrics=None,
        score=None,
        label=None,
        primary_issue=None,
        feedback_title=None,
        feedback_explanation=None,
        feedback_suggestion=None,
        rewrite_attempts=0,
        rewritten_text=None,
        rewrite_explanation=None,
        passed_evaluation=False
    )
    
    final_state = graph.invoke(initial_state)
    return final_state
