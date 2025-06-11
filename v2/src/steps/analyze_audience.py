# src/steps/analyze_audience.py
from src.steps.base_step import ConversationStep
from src.state import AgentState
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService

class AnalyzeAudienceStep(ConversationStep):
    """Analyzes the audience and asks for confirmation."""
    def execute(self, state: AgentState, llm_service: LanguageModelService, search_service: SearchService) -> tuple[AgentState, str]:
        state["current_step_name"] = "analyze_audience"
        # This step might be entered after clarifying goal, so save that last message.
        state["speaker_info"]["goal_metrics"] = state["messages"][-1].content
        
        print("\n🔍 Аналізую аудиторію...")

        event_name = state["event_info"].get("event_name", "")
        topic = state["speaker_info"].get("topic", "")
        search_results = search_service.run(f"{event_name} {topic} audience demographics attendees")

        analysis_prompt = f"""
        Проаналізуй аудиторію для виступу на тему "{topic}" на конференції "{event_name}".
        Додаткова інформація з пошуку: {search_results}
        Визнач основні сегменти аудиторії, їхні можливі інтереси та рівень знань.
        Відповідь дай українською мовою у вигляді короткого, структурованого аналізу.
        """
        analysis_content = llm_service.invoke(analysis_prompt)
        state["audience_analysis"] = {"content": analysis_content}

        # Prepare for feedback loop
        state["audience_approved"] = False
        state["audience_modification_count"] = 0
        
        confirmation_message = f"""
Ось попередній аналіз твоєї аудиторії:

{analysis_content}

Чи все вірно, чи хочеш щось додати або змінити? (так/додати/змінити)
        """
        return state, confirmation_message.strip()