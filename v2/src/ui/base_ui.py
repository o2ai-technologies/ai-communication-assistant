# src/ui/base_ui.py
from abc import ABC, abstractmethod
from src.state import AgentState

class BaseUI(ABC):
    """Abstract base class for user interfaces."""
    @abstractmethod
    def display_agent_message(self, message: str):
        pass

    @abstractmethod
    def get_user_input(self) -> str:
        pass

    @abstractmethod
    def show_summary(self, state: AgentState):
        pass

    @abstractmethod
    def show_help(self):
        pass