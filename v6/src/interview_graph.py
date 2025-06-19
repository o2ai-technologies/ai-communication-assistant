from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END, START
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode
from typing import Literal
from src.llm import llm
from src import prompts
from src.state import GraphState, Event, memory


tool = TavilySearch(max_results=10)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)

interview_builder = StateGraph(GraphState)

def interview_node(state: GraphState) -> GraphState:
    event = state.get("event", None)
    
    sys_prompt = prompts.context_builder_sys_prompt.format(event=event)
    ai_response = llm_with_tools.invoke([sys_prompt] + state["messages"])

    return {"messages": [ai_response],}
    
def human_input_node(state: GraphState) -> GraphState:
    pass
    
def parsing_node(state: GraphState) -> GraphState:
    messages = state["messages"]
    last_human_message = messages[-1] if messages else None
    event = state.get("event", None)
    parsing_instructions = prompts.parsing_interview_prompt.format(event=event,last_human_message=last_human_message, messages=messages)
    parsed_response = llm.with_structured_output(Event).invoke([HumanMessage(parsing_instructions)])
    

    return {"event": parsed_response.model_dump()}
    
def final_node(state: GraphState) -> GraphState:
    messages = state["messages"]
    last_human_message = messages[-1] if messages else None
    event = state.get("event", None)
    parsing_instructions = prompts.finalizing_interview_prompt.format(event=event,last_human_message=last_human_message, messages=messages)
    parsed_response = llm.with_structured_output(Event).invoke([HumanMessage(parsing_instructions)])
    return {
        "messages": [AIMessage(content=f"Чудово, тепер я зберу інформацію, яка допоможе тобі підготувати аргументи для твого виступу")]
    }

def goodbye_node(state: GraphState) -> GraphState:
    return {
        "messages": [AIMessage(content="Шкода, зустрінемось наступного разу.\n")]
    }
    
def is_interview_completed(event: Event) -> bool:
    if event \
    and event["is_going"] \
    and event["event"] \
    and event["topic"] \
    and event["goal"] \
    and event["target_audience"] \
    and event["audience_knowledge"] \
    and event["key_message"]:
        return True
    return False
    
def parsing_route_condition(state: GraphState) -> Literal['final', 'goodbye', 'interview']:
    """
    Determines the next step from the 'interview' node.
    Returns: "tools" if tool calls are present, "final" if no tool calls and the response is conclusive.
    """
    event = state.get("event", None)
    is_going = event.get("is_going", None) if event else None
    if is_interview_completed(event):
        state["event"] = Event()
        return "final"
    if is_going == False:
        state["event"] = Event()
        return "goodbye"
    
    return "interview"
    
def interview_route_condition(state: GraphState) -> Literal['human_input', 'tools']:
    """
    Determines the next step from the 'interview' node.
    Returns: "tools" if tool calls are present, "final" if no tool calls and the response is conclusive.
    """
    last_message = state["messages"][-1]
    is_tool_calls = isinstance(last_message, AIMessage) and last_message.tool_calls
    if is_tool_calls:
        return "tools"
    
    return "human_input"

interview_builder.add_node("interview", interview_node)
interview_builder.add_node("human_input", human_input_node)
interview_builder.add_node("parsing", parsing_node)
tool_node = ToolNode(tools=[tool])
interview_builder.add_node("tools", tool_node)
interview_builder.add_node("final", final_node)
interview_builder.add_node("goodbye", goodbye_node)


interview_builder.add_edge(START, "interview")
interview_builder.add_edge("human_input", "parsing")
interview_builder.add_conditional_edges(
    "parsing",
    parsing_route_condition
)
interview_builder.add_conditional_edges(
    "interview",
    interview_route_condition
)
interview_builder.add_edge("tools", "interview")
interview_builder.add_edge("final", END)
interview_builder.add_edge("goodbye", END)

interview_graph = interview_builder.compile(interrupt_before=["human_input"], checkpointer=memory)
# interview_graph = interview_builder.compile(interrupt_before=["human_input"])
