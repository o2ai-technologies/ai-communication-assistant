# src/steps/process_greeting_response.py
from src.steps.base_step import RepeatingStep
from src.state import AgentState
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService

class ProcessGreetingResponseStep(RepeatingStep):
    """
    Processes the user's response to the initial greeting and loops until
    the intent is clear.
    """
    def __init__(self):
        super().__init__(approval_flag='greeting_intent_clarified')

    def execute(self, state: AgentState, llm_service: LanguageModelService, search_service: SearchService) -> tuple[AgentState, str]:
        # The core logic of this method remains exactly the same.
        # It already sets the `greeting_intent_clarified` flag correctly.
        state["current_step_name"] = "process_greeting_response"
        user_response = state["messages"][-1].content.lower().strip()
        state[self.approval_flag] = False # Reset flag on each execution

        analysis_prompt = f"""
        Користувач відповів на питання "Готуєшся до виступу?": "{user_response}"
        Визнач чи це:
        - POSITIVE: користувач готується до виступу (так, готуюся, yes, звичайно, etc.)
        - NEGATIVE: користувач НЕ готується до виступу (ні, не готуюся, no, etc.)
        - UNCLEAR: відповідь незрозуміла або потребує уточнення
        Відповідь лише одним словом: POSITIVE, NEGATIVE, або UNCLEAR
        """
        intent = llm_service.invoke(analysis_prompt).strip().upper()

        if intent == "POSITIVE":
            state[self.approval_flag] = True
            return state, "Класно! Де будеш виступати? На якій конференції чи заході?"
        
        elif intent == "NEGATIVE":
            state[self.approval_flag] = True
            state["analysis_complete"] = True
            return state, "Зрозуміло! Якщо в майбутньому будеш готуватися до виступу, звертайся!"
        
        else: # UNCLEAR
            return state, "Вибач, не зовсім зрозумів. Ти готуєшся до якогось виступу? (так/ні)"