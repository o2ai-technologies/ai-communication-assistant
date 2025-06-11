# src/steps/base_step.py
from abc import ABC, abstractmethod
from src.state import AgentState
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService

class ConversationStep(ABC):
    """Abstract base class for a step in the conversation."""
    @abstractmethod
    def execute(
        self,
        state: AgentState,
        llm_service: LanguageModelService,
        search_service: SearchService
    ) -> tuple[AgentState, str]:
        """
        Executes the logic for this step.
        Returns the updated state and a message to display to the user.
        """
        pass

class RepeatingStep(ConversationStep):
    """
    Represents a step that loops until its specific approval_flag in the
    state is set to True.
    """
    def __init__(self, approval_flag: str):
        if not approval_flag:
            raise ValueError("approval_flag cannot be empty for a RepeatingStep")
        self.approval_flag = approval_flag
        super().__init__()