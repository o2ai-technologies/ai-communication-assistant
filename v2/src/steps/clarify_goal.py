# src/steps/clarify_goal.py
from src.steps.base_step import ConversationStep
from src.state import AgentState
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService

class ClarifyGoalStep(ConversationStep):
    """Saves the speaker's goal and asks a clarifying question."""
    def execute(self, state: AgentState, llm_service: LanguageModelService, search_service: SearchService) -> tuple[AgentState, str]:
        state["current_step_name"] = "clarify_goal"
        goal = state["messages"][-1].content
        state["speaker_info"]["goal"] = goal

        clarification_prompt = f"""
        Спікер хоче: {goal}
        Сформулюй питання, щоб перевести цю ціль в конкретні критерії досягнення.
        Наприклад, якщо мета "залучити студентів до школи", запитай "скільки студентів має прийти, щоб ціль була досягнута?"
        Дай коротку відповідь українською мовою.
        """
        clarifying_question = llm_service.invoke(clarification_prompt)
        return state, clarifying_question