from langgraph.graph import StateGraph
from langgraph.graph import END, START
from typing import Literal
from src.state import GraphState, memory
from src.interview_graph import interview_graph
from src.deep_research.graph import deep_research_graph
from src.arguments_graph import arguments_graph


builder = StateGraph(GraphState)
    
def parsing_route_condition(state: GraphState) -> Literal[END, 'deep_research_graph']:
    """
    Determines the next step from the 'interview' node.
    Returns: "tools" if tool calls are present, "final" if no tool calls and the response is conclusive.
    """
    event = state.get("event", None)
    is_going = event.get("is_going", None) if event else None
    if not is_going:
        return END
    
    return "deep_research_graph"

builder.add_node("interview_graph", interview_graph)
builder.add_node("deep_research_graph", deep_research_graph)
builder.add_node("arguments_graph", arguments_graph)


builder.add_edge(START, "interview_graph")
builder.add_conditional_edges("interview_graph", parsing_route_condition)
builder.add_edge("deep_research_graph", "arguments_graph")
builder.add_edge("arguments_graph", END)

graph = builder.compile(checkpointer=memory)
# graph = builder.compile()
