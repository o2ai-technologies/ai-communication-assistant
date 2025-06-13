from graph_state import GraphState
from langchain_core.messages import AIMessage


def greeting_node(state: GraphState) -> GraphState:
    """
    Kicks off the conversation with a greeting.
    This node runs first and its output is the agent's first message.
    """
    return {
        "messages": [AIMessage(content="Привіт! Готуєшся до виступу? (так/ні)")]
    }

def human_input_node(state: GraphState) -> GraphState:
    pass

def ask_event_node(state: GraphState) -> GraphState:
    return {
        "messages": [AIMessage(content="Розкажи до якої події готуєшся? Де будеш виступати?")]
    }

def final_node(state: GraphState) -> GraphState:
    return {
        "messages": [AIMessage(content="Вау, круто")]
    }

def goodbye_node(state: GraphState) -> GraphState:
    return {
        "messages": [AIMessage(content="Шкода, зустрінемось наступного разу")]
    }