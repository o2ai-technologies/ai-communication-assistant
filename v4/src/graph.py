from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from graph_state import GraphState
import src.nodes as nodes
import src.conditions as conditions

workflow = StateGraph(GraphState)
memory = MemorySaver()

workflow.add_node("greeting", nodes.greeting_node)
workflow.add_node("human_input", nodes.human_input_node)
workflow.add_node("ask_event", nodes.ask_event_node)
workflow.add_node("final", nodes.final_node)
workflow.add_node("goodbye", nodes.goodbye_node)

workflow.add_edge(START, "greeting")
workflow.add_edge("greeting", "human_input")
workflow.add_conditional_edges("human_input", conditions.analyse_greeting_feedback)
workflow.add_edge("ask_event", "final")
workflow.add_edge("final", END)
workflow.add_edge("goodbye", END)

graph = workflow.compile(interrupt_before=["human_input"], checkpointer=memory)
# graph = workflow.compile(interrupt_before=["human_input"])