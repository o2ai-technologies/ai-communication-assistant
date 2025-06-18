from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph import MessagesState
from src.llm import llm
from src import prompts
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel
from typing import Optional, Literal


tool = TavilySearch(max_results=10)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)


class EventDetails(BaseModel):
    name: Optional[str] = None
    dates: Optional[str] = None
    place: Optional[str] = None
    theme: Optional[str] = None
    attendees: Optional[str] = None
    stages: Optional[str] = None
    
class Event(BaseModel):
    is_going: Optional[bool] = None
    event: EventDetails = EventDetails()
    topic: Optional[str] = None
    goal: Optional[str] = None
    target_audience: Optional[str] = None
    audience_knowledge: Optional[str] = None
    key_message: Optional[str] = None
    

class GraphState(MessagesState):
    event: Event = Event()

memory = MemorySaver()
builder = StateGraph(GraphState)

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
        "messages": [AIMessage(content=f"Вау, круто!\n\nОсь підсумок: {parsed_response.model_dump()}")]
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

builder.add_node("interview", interview_node)
builder.add_node("human_input", human_input_node)
builder.add_node("parsing", parsing_node)
tool_node = ToolNode(tools=[tool])
builder.add_node("tools", tool_node)
builder.add_node("final", final_node)
builder.add_node("goodbye", goodbye_node)


builder.add_edge(START, "interview")
builder.add_edge("human_input", "parsing")
builder.add_conditional_edges(
    "parsing",
    parsing_route_condition
)
builder.add_conditional_edges(
    "interview",
    interview_route_condition
)
builder.add_edge("tools", "interview")
builder.add_edge("final", END)
builder.add_edge("goodbye", END)

graph = builder.compile(interrupt_before=["human_input"], checkpointer=memory)
