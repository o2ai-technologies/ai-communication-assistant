from langgraph.graph import StateGraph, END, START
from src.state import GraphState, memory
from src.interview_graph import interview_agent


builder = StateGraph(GraphState)

builder.add_node("interview_agent", interview_agent)


builder.add_edge(START, "interview_agent")
builder.add_edge("interview_agent", END)

graph = builder.compile(checkpointer=memory)
# graph = builder.compile()
