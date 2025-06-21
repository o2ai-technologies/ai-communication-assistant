from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END, START
from typing import Literal
from src.llm import llm
from src.prompts import arguments_prompt, argument_feedback_evaluation_prompt
from src.state import GraphState, memory


# Build the arguments_graph
arguments_builder = StateGraph(GraphState)

# Nodes
def generate_arguments_node(state: GraphState) -> GraphState:
    """
    Generates a list of arguments based on the deep research output and event details.
    """
    event = state.get("event", None)
    event_details = event.get("event", None)
    research_text = state.get("final_research_result", None)
    user_feedback = state["messages"][-1].content if not state.get("arguments_approved", False) else ""

    prompt = arguments_prompt.format(
        event_name=event_details["name"] or "N/A",
        event_details=f"{event_details["dates"]} {event_details["place"]} {event_details["theme"]} {event_details["attendees"]}",
        topic=event["topic"] or "N/A",
        goal=event["goal"] or "N/A",
        target_audience=event["target_audience"] or "N/A",
        audience_knowledge=event["audience_knowledge"] or "N/A",
        key_message=event["key_message"] or "N/A",
        research_text=research_text,
        user_feedback=user_feedback,
    )
    
    response = llm.invoke([HumanMessage(prompt)])
    
    return {"messages": [response]}

def human_input_node(state: GraphState) -> GraphState:
    pass

def final_node(state: GraphState) -> GraphState:
    return {
        "messages": [AIMessage(content=f"Чудово, чекатиму наступного твого виступу")]
    }

def parsing_node(state: GraphState) -> GraphState:
    user_feedback = state["messages"][-1].content
    generated_arguments_str = "\n".join(state["generated_arguments"])

    feedback_prompt = argument_feedback_evaluation_prompt.format(
        user_feedback=user_feedback,
        generated_arguments=generated_arguments_str
    )
    
    llm_response = llm.invoke(feedback_prompt).content.strip().upper()

    return {
        "arguments_approved": llm_response == "APPROVED"
    }

def next_step_router(state: GraphState) -> Literal["final", "generate_arguments"]:
    """
    Processes the user's feedback using an LLM and decides the next step.
    """
    is_approved = state.get("arguments_approved", False)

    if is_approved:
        return "final"
    else:
        return "generate_arguments"

arguments_builder.add_node("generate_arguments", generate_arguments_node)
arguments_builder.add_node("human_input", human_input_node)
arguments_builder.add_node("parsing", parsing_node)
arguments_builder.add_node("final", final_node)

arguments_builder.add_edge(START, "generate_arguments")
arguments_builder.add_edge("generate_arguments", "human_input")
arguments_builder.add_edge("human_input", "parsing")
arguments_builder.add_conditional_edges(
    "parsing",
    next_step_router,
    ["final", "generate_arguments"]
)
arguments_builder.add_edge("final", END)

arguments_graph = arguments_builder.compile(interrupt_before=["human_input"], checkpointer=memory)
# arguments_graph = arguments_builder.compile(interrupt_before=["human_input"])
