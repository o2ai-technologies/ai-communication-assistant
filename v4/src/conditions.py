from typing import Literal
from src.services.llm_service import llm_service
from src.graph_state import GraphState
from langgraph.graph import END
from src.nodes import NodeName

def analyse_greeting_feedback(state: GraphState) -> Literal["goodbye", "ask_event", "final"]:
    user_message = state["messages"][-1]
    analysis_prompt = f"""
    Користувач відповів на питання "Готуєшся до виступу?": "{user_message}"
    Визнач чи це:
    - POSITIVE: користувач готується до виступу (так, готуюся, yes, звичайно, etc.)
    - EVENT: користувач відповів що готується до виступу і вказав назву події до якої готується (так виступаю на конференції, готуюся до дзвінка з клієнтом, etc.)
    - NEGATIVE: відповів негативно
    - UNCLEAR: відповідь незрозуміла або потребує уточнення
    Відповідь лише одним словом: POSITIVE, NEGATIVE, EVENT або UNCLEAR
    """
    intent = llm_service.invoke(analysis_prompt).strip().upper()
    
    if intent == "POSITIVE":
        return "ask_event"
    elif intent == "EVENT":
        return "final"
    elif intent == "NEGATIVE":
        return "goodbye"
    else:
        return "human_input"

def should_continue(state: GraphState):
    """ Return the next node to execute """

    finished=state.get('event', {"finished": False}).get("finished", False)
    if finished:
        return NodeName.FINAL.value
    
    return NodeName.INTERVIEW.value