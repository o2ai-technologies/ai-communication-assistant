from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph import MessagesState
from src.llm import llm
from src import prompts
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver


tool = TavilySearch(max_results=3)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)

class GraphState(MessagesState):
    pass

memory = MemorySaver()
builder = StateGraph(GraphState)

def interview(state: GraphState) -> GraphState:
    sys_prompt = prompts.context_builder_sys_prompt

    return {"messages": [llm_with_tools.invoke([sys_prompt] + state["messages"])]}

builder.add_node("interview", interview)
tool_node = ToolNode(tools=[tool])
builder.add_node("tools", tool_node)


builder.add_edge(START, "interview")
builder.add_conditional_edges(
    "interview",
    tools_condition,
)
builder.add_edge("tools", "interview")

# builder.add_edge("interview", END)

graph = builder.compile(checkpointer=memory)
