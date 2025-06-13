# src/services/llm_service.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

class LanguageModelService:
    """A wrapper for the language model to decouple it from the main application."""
    def __init__(self, model_name: str, temperature: float = 0.7):
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

    def invoke(self, prompt: str) -> str:
        """Invokes the language model with a given prompt."""
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            # Handle potential API errors gracefully
            print(f"LLM Error: {e}")
            return "Вибачте, виникла помилка при обробці вашого запиту."
        
llm_service = LanguageModelService(model_name="gemini-2.0-flash")