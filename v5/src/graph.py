from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph import MessagesState
from src.llm import llm
from src import prompts
from src.event import EventDetails
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import PromptTemplate


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
    event: EventDetails

memory = MemorySaver()
builder = StateGraph(GraphState)

def interview(state: GraphState) -> GraphState:
    event_info = state["event"] if "event" in state else EventDetails()
    sys_prompt = PromptTemplate.from_template(prompts.context_builder_sys_prompt).invoke({"event_info": event_info}).to_string()

    return {"messages": [llm_with_tools.invoke([HumanMessage(content=sys_prompt)] + state["messages"])]}

def extract_event_info(state: GraphState) -> GraphState:
    sys_prompt = prompts.event_extractor_prompt

    # Filter out ToolMessages and combine all other messages into a single text
    messages_text = "\n\n".join([
        f"{msg.type.upper()}: {msg.content}"
        for msg in state["messages"]
        if not isinstance(msg, ToolMessage)
    ])

    # Create a single HumanMessage with the combined text
    combined_message = HumanMessage(content=messages_text)
    
    structured_llm = llm.with_structured_output(EventDetails)
    response = structured_llm.invoke([SystemMessage(content=sys_prompt), combined_message])

    return {"event": response.model_dump()}

builder.add_node("interview", interview_node)
builder.add_node("human_input", human_input_node)
builder.add_node("parsing", parsing_node)
tool_node = ToolNode(tools=[tool])
builder.add_node("tools", tool_node)
builder.add_node("extractor", extract_event_info)


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
builder.add_edge("interview", "extractor")
builder.add_edge("extractor", END)

graph = builder.compile()
