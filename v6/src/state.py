from langgraph.graph import MessagesState
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel, Field
from typing import Optional


class EventDetails(BaseModel):
    name: Optional[str] = Field(default=None, description="Назва конференції або заходу")
    dates: Optional[str] = Field(default=None, description="Дати проведення заходу")
    place: Optional[str] = Field(default=None, description="Місце проведення заходу")
    theme: Optional[str] = Field(default=None, description="Загальна тематика конференції або події")
    attendees: Optional[str] = Field(default=None, description="Очікувана кількість або тип аудиторії")
    stages: Optional[str] = Field(default=None, description="Інформація про секції або стейджі конференції")

class Event(BaseModel):
    is_going: Optional[bool] = Field(default=None, description="Чи дійсно спікер збирається виступати")
    event: EventDetails = Field(default_factory=EventDetails, description="Деталі події або конференції")
    topic: Optional[str] = Field(default=None, description="Тема виступу")
    goal: Optional[str] = Field(default=None, description="Мета спікера для участі у виступі")
    target_audience: Optional[str] = Field(default=None, description="Цільова аудиторія виступу")
    audience_knowledge: Optional[str] = Field(default=None, description="Що аудиторія вже знає про тему виступу")
    key_message: Optional[str] = Field(default=None, description="Основне повідомлення, яке спікер хоче донести")
    

class GraphState(MessagesState):
    event: Event = Event()

memory = MemorySaver()
