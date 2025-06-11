import chainlit as cl
from chatbot import InteractiveSpeakerPrepAgent
from langchain_core.messages import HumanMessage

@cl.on_chat_start
async def on_chat_start():
    # Initialize the agent
    agent = InteractiveSpeakerPrepAgent()
    cl.user_session.set("agent", agent)
    
    # Send welcome message
    await cl.Message(content="🎤 Speaker Preparation Agent").send()
    
    # Start with greeting
    response = agent._execute_step("greeting")
    if response:
        await cl.Message(content=response).send()

@cl.on_message
async def on_message(message: cl.Message):
    # Get the agent from session
    agent = cl.user_session.get("agent")
    
    # Add user message to state
    agent.state["messages"].append(HumanMessage(content=message.content))
    
    # Get current step
    current_step = agent.state["current_step"]
    
    # Process user input based on current step
    if current_step == "greeting":
        # After greeting, process the response
        agent.state["current_step"] = "process_greeting_response"
        response = agent._execute_step("process_greeting_response")
        if response:
            await cl.Message(content=response).send()
        
        # Move to next step
        if "Класно! Де будеш виступати?" in response:
            agent.state["current_step"] = "search_event"
        else:
            # Handle negative response
            agent.state["analysis_complete"] = True
            
    elif current_step == "process_greeting_response":
        # After processing greeting, search for event
        agent.state["current_step"] = "search_event"
        response = agent._execute_step("search_event")
        if response:
            await cl.Message(content=response).send()
            
    elif current_step == "search_event":
        # After event search, ask about goal
        agent.state["current_step"] = "ask_goal"
        response = agent._execute_step("ask_goal")
        if response:
            await cl.Message(content=response).send()
            
    elif current_step == "ask_goal":
        # After asking goal, clarify it
        agent.state["current_step"] = "clarify_goal"
        response = agent._execute_step("clarify_goal")
        if response:
            await cl.Message(content=response).send()
            
    elif current_step == "clarify_goal":
        # After clarifying goal, ask about stage
        agent.state["current_step"] = "ask_stage"
        response = agent._execute_step("ask_stage")
        if response:
            await cl.Message(content=response).send()
            
    elif current_step == "ask_stage":
        # After asking about stage, analyze audience
        agent.state["current_step"] = "analyze_audience"
        response = agent._execute_step("analyze_audience")
        if response:
            await cl.Message(content=response).send()
            
    elif current_step == "analyze_audience":
        # Process audience feedback
        agent.state["current_step"] = "process_audience_feedback"
        response = agent._execute_step("process_audience_feedback")
        if response:
            await cl.Message(content=response).send()
            
        # Check if audience is approved
        if agent.state.get("audience_approved", False):
            agent.state["current_step"] = "assess_knowledge"
            response = agent._execute_step("assess_knowledge")
            if response:
                await cl.Message(content=response).send()
                
    elif current_step == "process_audience_feedback":
        # Process audience feedback again
        response = agent._execute_step("process_audience_feedback")
        if response:
            await cl.Message(content=response).send()
            
        # Check if audience is approved
        if agent.state.get("audience_approved", False):
            agent.state["current_step"] = "assess_knowledge"
            response = agent._execute_step("assess_knowledge")
            if response:
                await cl.Message(content=response).send()
                
    elif current_step == "assess_knowledge":
        # Process knowledge feedback
        agent.state["current_step"] = "process_knowledge_feedback"
        response = agent._execute_step("process_knowledge_feedback")
        if response:
            await cl.Message(content=response).send()
            
        # Check if knowledge is approved
        if agent.state.get("knowledge_approved", False):
            agent.state["current_step"] = "generate_recommendation"
            response = agent._execute_step("generate_recommendation")
            if response:
                await cl.Message(content=response).send()
                
    elif current_step == "process_knowledge_feedback":
        # Process knowledge feedback again
        response = agent._execute_step("process_knowledge_feedback")
        if response:
            await cl.Message(content=response).send()
            
        # Check if knowledge is approved
        if agent.state.get("knowledge_approved", False):
            agent.state["current_step"] = "generate_recommendation"
            response = agent._execute_step("generate_recommendation")
            if response:
                await cl.Message(content=response).send()
                
    elif current_step == "generate_recommendation":
        # Process recommendation feedback
        agent.state["current_step"] = "process_recommendation_feedback"
        response = agent._execute_step("process_recommendation_feedback")
        if response:
            await cl.Message(content=response).send()
            
        # Check if recommendation is approved
        if agent.state.get("recommendation_approved", False):
            agent.state["analysis_complete"] = True
            
            # Show summary
            if agent.state.get("final_recommendation"):
                await cl.Message(content="✅ Analysis complete!").send()
                await cl.Message(content=f"🎯 Event: {agent.state.get('event_info', {}).get('event_name', 'Unknown')}").send()
                await cl.Message(content=f"📅 Date: {agent.state.get('event_info', {}).get('dates', 'TBD')}").send()
                await cl.Message(content=f"📝 Topic: {agent.state.get('speaker_info', {}).get('topic', 'Unknown')}").send()
                await cl.Message(content=f"🎯 Goal: {agent.state.get('speaker_info', {}).get('goal', 'Unknown')}").send()
                await cl.Message(content=f"💡 Recommendation: {agent.state.get('final_recommendation', 'None')}").send()
                
    elif current_step == "process_recommendation_feedback":
        # Process recommendation feedback again
        response = agent._execute_step("process_recommendation_feedback")
        if response:
            await cl.Message(content=response).send()
            
        # Check if recommendation is approved
        if agent.state.get("recommendation_approved", False):
            agent.state["analysis_complete"] = True
            
            # Show summary
            if agent.state.get("final_recommendation"):
                await cl.Message(content="✅ Analysis complete!").send()
                await cl.Message(content=f"🎯 Event: {agent.state.get('event_info', {}).get('event_name', 'Unknown')}").send()
                await cl.Message(content=f"📅 Date: {agent.state.get('event_info', {}).get('dates', 'TBD')}").send()
                await cl.Message(content=f"📝 Topic: {agent.state.get('speaker_info', {}).get('topic', 'Unknown')}").send()
                await cl.Message(content=f"🎯 Goal: {agent.state.get('speaker_info', {}).get('goal', 'Unknown')}").send()
                await cl.Message(content=f"💡 Recommendation: {agent.state.get('final_recommendation', 'None')}").send()
