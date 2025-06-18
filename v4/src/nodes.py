from src.graph_state import GraphState, Event
from langchain_core.messages import AIMessage
from enum import Enum

from src.services import llm_service, search_service
from langchain_core.messages import HumanMessage


class NodeName(Enum):
    GREETING = 'greeting'
    INTERVIEW = 'interview'
    HUMAN_INPUT = 'human_input'
    ASK_EVENT = 'ask_event'
    FINAL = 'final'
    GOODBYE = 'goodbye'

def greeting_node(state: GraphState) -> GraphState:
    """
    Kicks off the conversation with a greeting.
    This node runs first and its output is the agent's first message.
    """
    return {
        "messages": [AIMessage(content="Привіт! Готуєшся до виступу? (так/ні)\n")]
    }

def human_input_node(state: GraphState) -> GraphState:
    pass

#     question_instructions = f"""You are an public speaking expert tasked with interviewing a speaker to learn about an event he is preapering for. 
# Take into account information provided by the user: {user_message}

# If it is no message from user your taks is to greet user ask whether or not it is going to any event.
# Possible answers can be yes (or similar clearly indicates that it is going to event), no (or similar clearly indicates that user is not going to any event). If answer is unclear agent should ask follow up questions to get that information from the user.

# After greeting step agent should repeatedly ask user to get following information:
# - event name
# - event details (event name, dates, place, main theme, attendees, stages - get as much information as possible. Use web search for this task)
# - topic (what is the topic he is participating at this event with)
# - goal (speaker's internal goal - why it is important for him to attend at this event)
# - clarify goal (Formulate a question to translate this goal into specific achievement criteria.
# For example, if the goal is "to attract students to the school," ask "how many students need to enroll for the goal to be considered achieved?")
# - target audience (search information about potential target audience related to this event and the topic. Use web search for this task)
# Here is alse event object {state["event"]}
# When parsing take into account already existing event object and update only fields 
# In any moment user is able to clearly articulate that he wants to proceed further with available information.
# In this case you should mark `finished` field as True. In other cases 
# """
def interview_node(state: GraphState) -> GraphState:
    messages = state["messages"]
    question_instructions = f"""You are an public speaking expert tasked with interviewing a speaker to learn about an event he is preapering for. 
Here is conversation history between you and user: {messages}

If there are no messages from user your taks is to greet user ask whether or not it is going to any event.
Possible answers can be yes (or similar clearly indicates that it is going to event), no (or similar clearly indicates that user is not going to any event). If answer is unclear agent should ask follow up questions to get that information from the user.

After greeting step you should repeatedly ask user to get following required information:
- event name
- topic (topic user will be presenting)

Important: field `message` - should contain your question to the user if you have something to clarify
In any moment user is able to clearly articulate that he wants to proceed further with available information.
In this case you should mark `finished` field as True.
If you have all required information place 'Thank you' as a `message` field and mark `finished` as True.
"""
    structured_llm = llm_service.llm_service.llm.with_structured_output(Event)
    # tools = [search_service.search_service.search_tool]
    # sturctured_llm_with_tools = structured_llm.bind_tools(tools)
    response = structured_llm.invoke([HumanMessage(question_instructions)])
    
    return {
        "messages": [AIMessage(content=response.message)],
        "event": response.model_dump(),
    }

def ask_event_node(state: GraphState) -> GraphState:
    return {
        "messages": [AIMessage(content="Розкажи до якої події готуєшся? Де будеш виступати?\n")]
    }

def final_node(state: GraphState) -> GraphState:
    return {
        "messages": [AIMessage(content="Вау, круто!\n")]
    }

def goodbye_node(state: GraphState) -> GraphState:
    return {
        "messages": [AIMessage(content="Шкода, зустрінемось наступного разу.\n")]
    }