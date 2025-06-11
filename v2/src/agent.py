# src/agent.py
from src.state import AgentState
from src.steps.ask_and_process_stage import AskAndProcessStageStep
from src.steps.process_feedback import ProcessFeedbackStep
from src.ui.base_ui import BaseUI
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService
from langchain_core.messages import HumanMessage

# Import all step classes
from src.steps.greeting import GreetingStep
from src.steps.process_greeting_response import ProcessGreetingResponseStep
from src.steps.search_event import SearchEventStep
from src.steps.ask_goal import AskGoalStep
from src.steps.clarify_goal import ClarifyGoalStep
from src.steps.analyze_audience import AnalyzeAudienceStep
from src.steps.assess_knowledge import AssessKnowledgeStep
from src.steps.generate_recommendation import GenerateRecommendationStep
from src.steps.base_step import RepeatingStep

class InteractiveSpeakerPrepAgent:
    """Orchestrates the conversation flow by executing a sequence of steps."""
    def __init__(
        self,
        llm_service: LanguageModelService,
        search_service: SearchService,
        ui: BaseUI
    ):
        self.llm_service = llm_service
        self.search_service = search_service
        self.ui = ui
        
        # The sequence of steps is now a list of objects, including our reusable feedback steps
        self.steps = [
            GreetingStep(),
            ProcessGreetingResponseStep(),
            SearchEventStep(),
            AskGoalStep(),
            ClarifyGoalStep(),
            AskAndProcessStageStep(),
            AnalyzeAudienceStep(),
            ProcessFeedbackStep(
                item_name="аналізу аудиторії",
                item_key="audience_analysis",
                approval_flag="audience_approved",
            ),
            AssessKnowledgeStep(),
            ProcessFeedbackStep(
                item_name="оцінки знань",
                item_key="knowledge_assessment",
                approval_flag="knowledge_approved",
            ),
            GenerateRecommendationStep(),
            ProcessFeedbackStep(
                item_name="фінальної рекомендації",
                item_key="final_recommendation",
                approval_flag="recommendation_approved",
            )
        ]
        self.state = self._initialize_state()

    def _initialize_state(self) -> AgentState:
        """Initializes or resets the agent's state."""
        # Add all approval flags and counters here
        return {
            "messages": [],
            "event_info": {},
            "speaker_info": {},
            "analysis_complete": False,
            "user_input_flag": True,
            "current_step_name": "initialization",
            "audience_analysis": {},
            "knowledge_assessment": {},
            "final_recommendation": "",
            "audience_approved": False,
            "audience_modification_count": 0,
            "knowledge_approved": False,
            "knowledge_modification_count": 0,
            "recommendation_approved": False,
            "recommendation_modification_count": 0,
        }

    def run(self):
        """Main interactive loop for the agent. Handles step progression and feedback loops."""
        self.state = self._initialize_state()
        step_index = 0
        user_input = ""
        agent_message = ""
        should_wait_for_input = False

        while step_index < len(self.steps):
            if should_wait_for_input:
                user_input = self.ui.get_user_input()
            if user_input.lower() in ['quit', 'exit', 'вихід', 'стоп']:
                self.ui.display_agent_message("Розмову завершено. До побачення!")
                break
            
            self.state["messages"].append(HumanMessage(content=user_input))
            
            current_step = self.steps[step_index]
            self.state, agent_message = current_step.execute(self.state, self.llm_service, self.search_service)
            should_wait_for_input = not self.state.pop('__skip_next_input', False)
            
            if agent_message:
                self.ui.display_agent_message(agent_message)
            
            if self.state["analysis_complete"]:
                break

            should_advance = True
            if isinstance(current_step, RepeatingStep):
                if not self.state.get(current_step.approval_flag, False):
                    should_advance = False
            
            if should_advance:
                step_index += 1

        self.ui.show_summary(self.state)