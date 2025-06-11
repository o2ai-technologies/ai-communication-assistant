# src/steps/assess_knowledge.py
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService
from src.state import AgentState
from src.steps.base_step import ConversationStep

class AssessKnowledgeStep(ConversationStep):
    """Assesses audience knowledge and asks for confirmation."""
    def execute(self, state: AgentState, llm_service: LanguageModelService, search_service: SearchService) -> tuple[AgentState, str]:
        state["current_step_name"] = "assess_knowledge"
        print("\n🧠 Оцінюю знання аудиторії...")
        
        topic = state["speaker_info"].get("topic")
        audience_analysis = state["audience_analysis"].get("content")

        assessment_prompt = f"""
        Базуючись на темі "{topic}" та аналізі аудиторії: '{audience_analysis}',
        опиши, що ця аудиторія ймовірно вже зараз знає про цю тему, а що їй треба дізнатися для досягнення мети спікера.
        Відповідь українською мовою, детально та структуровано.
        """
        assessment_content = llm_service.invoke(assessment_prompt)
        state["knowledge_assessment"] = {"content": assessment_content}
        state["knowledge_approved"] = False
        state["knowledge_modification_count"] = 0

        return state, f"Ось оцінка знань аудиторії:\n\n{assessment_content}\n\nТи згоден з цим?"