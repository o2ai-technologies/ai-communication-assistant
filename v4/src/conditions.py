from typing import Literal
from src.llm_service import llm_service
from src.graph_state import GraphState

def analyse_greeting_feedback(state: GraphState) -> Literal["goodbye", "ask_event", "final"]:
    user_message = state["messages"][-1]
    analysis_prompt = f"""
    Користувач відповів на питання "Готуєшся до виступу?": "{user_message}"
    Визнач чи це:
    - POSITIVE: користувач готується до виступу (так, готуюся, yes, звичайно, etc.)
    - EVENT: користувач відповів що готується до виступу і вказав назву події до якої готується (так виступаю на конференції, готуюся до дзвінка з клієнтом, etc.)
    - NEGATIVE: відповів негативно або незрозуміло
    Відповідь лише одним словом: POSITIVE, NEGATIVE, або EVENT
    """
    intent = llm_service.invoke(analysis_prompt).strip().upper()
    
    if intent == "POSITIVE":
        return "ask_event"
    elif intent == "EVENT":
        return "final"
    else:
        return "goodbye"