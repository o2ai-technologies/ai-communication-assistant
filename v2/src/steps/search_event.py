# src/steps/search_event.py
from src.steps.base_step import ConversationStep
from src.state import AgentState
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService
from langchain_core.utils.json import parse_json_markdown
import json
from datetime import datetime

class SearchEventStep(ConversationStep):
    """
    Searches for event information, extracts structured data into the state,
    and formulates a friendly response to the user.
    """
    def execute(self, state: AgentState, llm_service: LanguageModelService, search_service: SearchService) -> tuple[AgentState, str]:
        state["current_step_name"] = "search_event"
        event_name = state["messages"][-1].content

        current_year = datetime.now().year
        next_year = current_year + 1
        
        print(f"\n🔍 Шукаю інформацію про '{event_name}' на {current_year}/{next_year} рік...")
        
        search_query = f"{event_name} conference {current_year} or {next_year} details agenda speakers"
        search_results = search_service.run(search_query)

        json_extraction_prompt = f"""
        Проаналізуй наступні результати пошуку про конференцію '{event_name}'.
        Витягни ключову інформацію та поверни її **виключно у форматі JSON** у Markdown-блоці.

        Ключі для JSON:
        - "event_name": точна назва події
        - "dates": дати проведення (якщо знайдено)
        - "place": місце проведення (місто, країна, або "online")
        - "theme": основна тематика або слоган конференції
        - "attendees": очікувана кількість відвідувачів (якщо знайдено)
        - "stages": список назв стейджів/секцій (якщо є)
        - "target_audience": опис цільової аудиторії

        Якщо для якогось ключа інформація відсутня, використовуй значення `null`.

        Результати пошуку:
        ---
        {search_results}
        ---
        """

        json_response = llm_service.invoke(json_extraction_prompt)
        
        try:
            extracted_data = parse_json_markdown(json_response)
            state["event_info"] = extracted_data
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            print(f"⚠️  Не вдалося розпарсити JSON, зберігаю базову інформацію. Помилка: {e}")
            state["event_info"] = {"event_name": event_name}

        conversational_prompt = f"""
        На основі наступної структурованої інформації про подію, сформулюй коротке, дружнє повідомлення для спікера українською мовою.

        Інформація про подію:
        {json.dumps(state["event_info"], indent=2, ensure_ascii=False)}

        У повідомленні:
        1. Підтверди, що ти знайшов інформацію.
        2. Згадай 2-3 найважливіші деталі (наприклад, назву, тематику, місце проведення). Не згадуй поля зі значенням `null`.
        3. Заверши повідомлення природним та дружнім питанням про те, на яку тему буде виступ користувача.
        """

        response_message = llm_service.invoke(conversational_prompt)

        return state, response_message