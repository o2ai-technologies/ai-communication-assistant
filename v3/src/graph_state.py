from typing import Dict, Any
from langgraph.graph import MessagesState

class GraphState(MessagesState):
    """
    Represents the state of our graph.

    Attributes:
        messages: The history of messages in the conversation. Inherited from MessagesState
        event_info: Information about the event.
        speaker_info: Information about the speaker.
        audience_analysis: Analysis of the target audience.
        knowledge_assessment: Assessment of the audience's knowledge.
        final_recommendation: The final generated recommendation.
        # Feedback flags can be managed more dynamically if needed
        # but for simplicity, we can keep a generic one.
        feedback_approved: A flag to indicate if feedback was approved.
    """
    event_info: Dict[str, Any]
    speaker_info: Dict[str, Any]
    audience_analysis: Dict[str, Any]
    knowledge_assessment: Dict[str, Any]
    final_recommendation: str
    feedback_approved: bool