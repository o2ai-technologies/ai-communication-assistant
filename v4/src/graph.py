from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from graph_state import GraphState
import src.nodes as nodes
from src.nodes import NodeName
import src.conditions as conditions

workflow = StateGraph(GraphState)
memory = MemorySaver()

workflow.add_node(NodeName.INTERVIEW.value, nodes.interview_node)
workflow.add_node(NodeName.HUMAN_INPUT.value, nodes.human_input_node)
workflow.add_node(NodeName.FINAL.value, nodes.final_node)
# workflow.add_node(NodeName.GREETING.value, nodes.greeting_node)
# workflow.add_node(NodeName.HUMAN_INPUT.value, nodes.human_input_node)
# workflow.add_node(NodeName.ASK_EVENT.value, nodes.ask_event_node)
# workflow.add_node(NodeName.FINAL.value, nodes.final_node)
# workflow.add_node(NodeName.GOODBYE.value, nodes.goodbye_node)

workflow.add_edge(START, NodeName.INTERVIEW.value)
workflow.add_edge(NodeName.INTERVIEW.value, NodeName.HUMAN_INPUT.value)
workflow.add_conditional_edges(NodeName.HUMAN_INPUT.value,
                               conditions.should_continue,
                               [NodeName.INTERVIEW.value, NodeName.FINAL.value])
workflow.add_edge(NodeName.FINAL.value, END)

# workflow.add_edge(START, NodeName.GREETING.value)
# workflow.add_edge(NodeName.GREETING.value, NodeName.HUMAN_INPUT.value)
# workflow.add_conditional_edges(NodeName.HUMAN_INPUT.value,
#                                conditions.analyse_greeting_feedback,
#                                [NodeName.ASK_EVENT.value, NodeName.FINAL.value, NodeName.GOODBYE.value, NodeName.HUMAN_INPUT.value])
# workflow.add_edge(NodeName.ASK_EVENT.value, NodeName.FINAL.value)
# workflow.add_edge(NodeName.FINAL.value, END)
# workflow.add_edge(NodeName.GOODBYE.value, END)

graph = workflow.compile(interrupt_before=[NodeName.HUMAN_INPUT.value], checkpointer=memory)
# graph = workflow.compile(interrupt_before=["human_input"])