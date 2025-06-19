import chainlit as cl
from src.graph import graph
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage, ToolMessage

@cl.on_chat_start
async def on_start():
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")
    
    for msg, _ in graph.stream({}, stream_mode="messages", config=RunnableConfig(callbacks=[cb], **config)):
        if (msg.content):
            await final_answer.stream_token(msg.content)

    await final_answer.send()

@cl.on_message
async def on_message(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()  
    final_answer = cl.Message(content="")
    sub_state = graph.get_state(config, subgraphs=True).tasks[0].state
    sub_cfg = sub_state.config
    sub_next_node, = sub_state.next
    
    
    graph.update_state(sub_cfg, {"messages": msg.content}, sub_next_node)
    for msg, _ in graph.stream(None, stream_mode="messages", config=RunnableConfig(callbacks=[cb], **config)):
        if (
            msg.content
            and not isinstance(msg, HumanMessage)
            and not isinstance(msg, ToolMessage)
        ):
            await final_answer.stream_token(msg.content)

    await final_answer.send()
