# src/state.py
from typing import Dict, List, TypedDict, Annotated
from langchain.schema import BaseMessage
import operator

# State is now in its own file for clarity and reuse.
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    event_info: Dict
    speaker_info: Dict
    analysis_complete: bool
    user_input_flag: bool
    current_step_name: str
    audience_analysis: Dict
    knowledge_assessment: Dict
    final_recommendation: str