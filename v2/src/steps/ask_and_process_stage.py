# src/steps/ask_and_process_stage.py
from src.steps.base_step import RepeatingStep
from src.state import AgentState
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService

class AskAndProcessStageStep(RepeatingStep):
    """
    A conditional step that asks about the event stage/track only if the
    event information suggests they exist. Otherwise, it skips itself.
    """
    def __init__(self):
        super().__init__(approval_flag='stage_info_processed')

    def execute(self, state: AgentState, llm_service: LanguageModelService, search_service: SearchService) -> tuple[AgentState, str]:
        state["current_step_name"] = "ask_and_process_stage"
        
        # Check if we have already asked the question and are now processing the answer.
        if state.get('stage_question_asked'):
            stage_name = state["messages"][-1].content
            state["speaker_info"]["stage"] = stage_name
            state[self.approval_flag] = True
            state['__skip_next_input'] = True # skip asking user for input
            return state, "" 

        event_info = state.get("event_info", {})
        event_str = str(event_info).lower()
        keywords = ["стейдж", "секція", "track", "stage", "потік"]

        # Check if the event info contains any keywords indicating multiple stages.
        if any(word in event_str for word in keywords):
            state['stage_question_asked'] = True
            state[self.approval_flag] = False
            return state, "Зрозуміло. На якій секції/стейджі ти будеш виступати?"
        else:
            state['stage_question_asked'] = False
            state[self.approval_flag] = True
            return state, ""