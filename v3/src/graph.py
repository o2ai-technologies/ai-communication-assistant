from langgraph.graph import StateGraph, END
from graph_state import GraphState
import nodes as nodes

# Define the graph builder
workflow = StateGraph(GraphState)

# 1. Add the nodes
workflow.add_node("greeting", nodes.greeting_node)
workflow.add_node("search_event", nodes.search_event_node)
workflow.add_node("process_greeting", nodes.process_greeting_node)
workflow.add_node("analyze_audience", nodes.analyze_audience_node)
workflow.add_node("process_feedback", nodes.process_feedback_node)
# ... add other nodes like assess_knowledge, generate_recommendation etc.

# 2. Define the edges
workflow.set_entry_point("greeting")
workflow.add_edge("greeting", "process_greeting")

def should_exit_after_greeting(state: GraphState) -> str:
    """Decide whether to continue or end the conversation."""
    if "ні" in state["messages"][-1].content.lower():
        return "end"
    return "continue"

workflow.add_conditional_edges(
    "process_greeting",
    should_exit_after_greeting,
    {
        "end": END,
        "continue": "search_event", # Or the next logical step
    }
)

workflow.add_edge("search_event", "analyze_audience")
workflow.add_edge("analyze_audience", "process_feedback")

def after_feedback_router(state: GraphState) -> str:
    """Routes to the next step or loops back for more feedback."""
    if state["feedback_approved"]:
        # Move to the next major step
        # return "assess_knowledge" # Example: next step is knowledge assessment
        return "end"
    # Loop back to the feedback node to await corrected input
    return "process_feedback" 

# This conditional edge creates the feedback loop
workflow.add_conditional_edges(
    "process_feedback",
    after_feedback_router,
    {
        # In a real scenario, you would have a node for each step
        # "assess_knowledge": "analyze_audience", # Replace with actual next node
        "end": END,
        "process_feedback": "analyze_audience", # Loop back to get new input for analysis
    }
)

# 3. Compile the graph and set interrupts
# The graph will pause after any node in this list finishes.
# This is how the agent sends a message and waits for your reply.
interrupting_nodes = ["greeting", "search_event", "process_feedback"]
graph = workflow.compile(interrupt_after=interrupting_nodes)