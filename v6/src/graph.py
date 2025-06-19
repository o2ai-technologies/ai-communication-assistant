from langgraph.graph import StateGraph, END, START
from src.state import GraphState, memory
from src.interview_graph import interview_graph
from src.deep_research.graph import deep_research_graph


builder = StateGraph(GraphState)

builder.add_node("interview_graph", interview_graph)
builder.add_node("deep_research_graph", deep_research_graph)


builder.add_edge(START, "interview_graph")
builder.add_edge("interview_graph", "deep_research_graph")
builder.add_edge("deep_research_graph", END)

graph = builder.compile(checkpointer=memory)
# graph = builder.compile()
