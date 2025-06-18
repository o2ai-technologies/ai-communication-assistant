import chainlit as cl
from src.graph import graph
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage, ToolMessage
from typing import cast

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
async def on_message(message: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}    
    final_answer = cl.Message(content="")

    for msg, metadata in graph.stream({"messages": [HumanMessage(content=message.content)]}, stream_mode="messages", config=config):
        if (
            msg.content
            and not isinstance(msg, HumanMessage)
            and not isinstance(msg, ToolMessage)
        ):
            await final_answer.stream_token(msg.content)

    await final_answer.send()