# src/steps/generate_recommendation.py
from src.steps.base_step import ConversationStep
from src.state import AgentState
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService

class GenerateRecommendationStep(ConversationStep):
    """
    Synthesizes all gathered information into a final, actionable recommendation
    for the speaker's core message.
    """
    def execute(
        self,
        state: AgentState,
        llm_service: LanguageModelService,
        search_service: SearchService
    ) -> tuple[AgentState, str]:
        """
        Executes the logic to generate the final recommendation.

        Returns:
            A tuple containing the updated state and a message for the user,
            presenting the recommendation and asking for feedback.
        """
        state["current_step_name"] = "generate_recommendation"
        print("\n💡 Генерую фінальні рекомендації...")

        # --- Gather all context from the state ---
        speaker_info = state.get("speaker_info", {})
        audience_analysis = state.get("audience_analysis", {})
        knowledge_assessment = state.get("knowledge_assessment", {})

        topic = speaker_info.get('topic', 'Невідома')
        goal = speaker_info.get('goal', 'Невідома')
        audience_content = audience_analysis.get('content', 'Немає даних')
        knowledge_content = knowledge_assessment.get('content', 'Немає даних')

        # --- Create a comprehensive prompt for the LLM ---
        recommendation_prompt = f"""
        You are an expert public speaking coach. Your task is to synthesize all available information and formulate one clear, powerful key message that a speaker should deliver to achieve their goal.

        **CONTEXT:**
        1.  **Speaker's Topic:** {topic}
        2.  **Speaker's Goal:** {goal}
        3.  **Audience Analysis:** {audience_content}
        4.  **Audience's Current Knowledge:** {knowledge_content}

        **TASK:**
        Based on all the context, create the single most important message or takeaway for the audience. This message should be memorable, actionable, and directly help the speaker achieve their stated goal.

        The message should be formulated in Ukrainian. Return only the key message itself, without any extra explanations or introductions.
        """

        # --- Generate the recommendation ---
        recommendation_content = llm_service.invoke(recommendation_prompt)

        # --- Update state and prepare for the feedback loop ---
        state["final_recommendation"] = {"content": recommendation_content}
        state["recommendation_approved"] = False
        state["recommendation_modification_count"] = 0

        # --- Create the confirmation message for the user ---
        confirmation_message = f"""
На основі всього, що ми обговорили, для досягнення твоєї цілі я вважаю, що ключова думка, яку аудиторія має винести з виступу, повинна бути такою:

"{recommendation_content}"

Чи згоден ти з цією основною рекомендацією? Можливо, хочеш щось змінити або доповнити?
        """.strip()

        return state, confirmation_message