# src/steps/ask_goal.py
from src.steps.base_step import ConversationStep
from src.state import AgentState
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService

class AskGoalStep(ConversationStep):
    """Saves the event topic and asks for the speaker's goal."""
    def execute(self, state: AgentState, llm_service: LanguageModelService, search_service: SearchService) -> tuple[AgentState, str]:
        state["current_step_name"] = "ask_goal"
        topic = state["messages"][-1].content
        state["speaker_info"]["topic"] = topic
        return state, "Чому ти погодився там виступити? Яка твоя мета?"