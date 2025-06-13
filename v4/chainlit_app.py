import chainlit as cl
from src.graph import graph
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage


@cl.on_chat_start
async def on_start():
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")
    
    for msg, metadata in graph.stream({}, stream_mode="messages", config=RunnableConfig(callbacks=[cb], **config)):
        if (
            msg.content
        ):
            await final_answer.stream_token(msg.content)

    await final_answer.send()
    

@cl.on_message
async def on_message(msg: HumanMessage):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")
    next_node, = graph.get_state(config).next
    
    graph.update_state(config, {"messages": msg.content}, next_node)
    for msg, metadata in graph.stream(None, stream_mode="messages", config=RunnableConfig(callbacks=[cb], **config)):
        if (
            msg.content
        ):
            await final_answer.stream_token(msg.content)

    await final_answer.send()