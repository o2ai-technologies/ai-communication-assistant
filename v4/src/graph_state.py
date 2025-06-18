from langgraph.graph import MessagesState
from pydantic import BaseModel, Field
from typing import Optional
    
    
class EventDetails(BaseModel):
    name: str = Field(
        description="Name of the event (e.g. Dou Day 2025, Meeting with C-level management, Sales call with client)"
    ),
    dates: str = Field(
        description="When does the event will take place (e.g. June 15 2025 9:00 AM, tomorrow afternoon, in 5 hours)"
    ),
    place: str = Field(
        description="Where does the event will take place (e.g. Kyiv at Exhibition Center, Apple's office)"
    ),
    theme: str = Field(
        description="Main theme of the event (e.g. How AI will change the surface of the tech world)"
    ),
    attendees: str = Field(
        description="How many participants expected"
    ),
    stages: Optional[str] = Field(
        description="What stages/sections/tracks will be at this event"
    )
    
class Event(BaseModel):
    is_going: Optional[bool] = None
    event_name: Optional[str] = None
    topic: Optional[str] = None
    finished: bool = False
    message: Optional[str] = None
    # is_going: bool = Field(
    #     description="Flag to determine whether user is going to any event"
    # ),
    # event_name: str = Field(
    #     description="Name of the event (e.g. Dou Day 2025, Meeting with C-level management, Sales call with client)"
    # ),
    # event_dates: str = Field(
    #     description="When does the event will take place (e.g. June 15 2025 9:00 AM, tomorrow afternoon, in 5 hours)"
    # ),
    # event_place: str = Field(
    #     description="Where does the event will take place (e.g. Kyiv at Exhibition Center, Apple's office)"
    # ),
    # event_theme: str = Field(
    #     description="Main theme of the event (e.g. How AI will change the surface of the tech world)"
    # ),
    # event_attendees: str = Field(
    #     description="How many participants expected"
    # ),
    # event_stages: Optional[str] = Field(
    #     description="What stages/sections/tracks will be at this event"
    # )
    # topic: str = Field(
    #     description="What the topic speaker is participating at the event with"
    # ),
    # goal: str = Field(
    #     description="Speaker's internal goal. Why the topic is important for the speaker"
    # ),
    # target_audience: str = Field(
    #     description="Potential audience that will be interested in speaker's topic at the event"
    # ),
    # finished: bool = Field(
    #     False,
    #     description="Flag indicates that gathering information about the event is finished and workflow can go further"
    # ),
    # message: str = Field(
    #     description="Next question to get further information about event from user"
    # )

class GraphState(MessagesState):
    """
    Represents the state of our graph.

    Attributes:
        messages: The history of messages in the conversation. Inherited from MessagesState
        event: Information about the event.
    """
    event: Event