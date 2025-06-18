from graph_state import GraphState
from services.llm_service import LanguageModelService
from services.search_service import SearchService
from langchain_core.messages import AIMessage

from config import LLM_MODEL_NAME, MAX_SEARCH_RESULTS

llm_service = LanguageModelService(model_name=LLM_MODEL_NAME)
search_service = SearchService(max_results=MAX_SEARCH_RESULTS)

def greeting_node(state: GraphState) -> dict:
    """
    Kicks off the conversation with a greeting.
    This node runs first and its output is the agent's first message.
    """
    return {
        "messages": [AIMessage(content="Привіт! Готуєшся до виступу? (так/ні)")]
    }

def process_greeting_node(state: GraphState) -> dict:
    """Searches for event info based on the latest user message."""
    user_input = state["messages"][-1].content
    
    if "ні" in user_input.lower():
        return {
        "messages": [AIMessage(content="Добре, бувай!")]
    }

    return {
        "messages": [AIMessage(content="Де ти плануєш виступити?")]
    }


def search_event_node(state: GraphState) -> dict:
    """Searches for event info based on the latest user message."""

    print("🔍 Шукаю інформацію про '------'...")
    
    # Logic to search for the event...
    event_info = {"name": "DOU Day 2025", "date": "May 16–17, 2025"}
    message = f"Так, я знайшов інформацію про {event_info['name']}. На яку тему плануєш виступити?"
    
    # When updating other state parts, return a dictionary.
    # Notice we are NOT doing `state["messages"] + ...` anymore.
    # We are only providing the NEW message.
    return {
        "event_info": event_info,
        "messages": [AIMessage(content=message)],
    }

def analyze_audience_node(state: GraphState) -> dict:
    """Analyzes the target audience."""
    print("🔍 Аналізую аудиторію...")
    
    analysis = "## Аналіз аудиторії DOU Day 2025: ...\n\nЧи все вірно, чи хочеш щось додати або змінити? (так/змінити)"
    
    # Update state and provide the new message
    return {
        "audience_analysis": {"summary": analysis},
        "messages": [AIMessage(content=analysis)],
        "feedback_approved": False,
    }
    
def process_feedback_node(state: GraphState) -> dict:
    """Processes user feedback."""
    user_input = state["messages"][-1].content.lower()
    
    if "так" in user_input or "давай далі" in user_input:
        # User is satisfied. Update the flag. No new message needed.
        return {"feedback_approved": True}
    
    # User wants changes. Send a new message.
    message = AIMessage(content="Зрозумів. Що саме хочеш змінити або додати?")
    return {"feedback_approved": False, "messages": [message]}

# ... all other nodes would follow this simplified pattern.