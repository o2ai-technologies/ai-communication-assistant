# src/steps/greeting.py
from src.steps.base_step import ConversationStep
from src.state import AgentState
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService

class GreetingStep(ConversationStep):
    """The initial greeting step."""
    def execute(self, state: AgentState, llm_service: LanguageModelService, search_service: SearchService) -> tuple[AgentState, str]:
        state["current_step_name"] = "greeting"
        message = "Привіт! Готуєшся до виступу?"
        return state, message