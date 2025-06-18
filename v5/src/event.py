from langgraph.graph import MessagesState
from pydantic import BaseModel, Field
from typing import Optional


class EventDetails(BaseModel):
    name: str = Field(
        default="",
        description="Name of the event (e.g. Dou Day 2025, Meeting with C-level management, Sales call with client)"
    )
    dates: str = Field(
        default="",
        description="When does the event will take place (e.g. June 15 2025 9:00 AM, tomorrow afternoon, in 5 hours)"
    )
    place: str = Field(
        default="",
        description="Where does the event will take place (e.g. Kyiv at Exhibition Center, Apple's office)"
    )
    theme: str = Field(
        default="",
        description="Main theme of the event (e.g. How AI will change the surface of the tech world)"
    )
    attendees: str = Field(
        default="",
        description="How many participants expected"
    )
    stages: Optional[str] = Field(
        default="",
        description="What stages/sections/tracks will be at this event"
    )
