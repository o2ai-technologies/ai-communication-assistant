# src/steps/process_feedback.py
from src.steps.base_step import RepeatingStep
from src.state import AgentState
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService

class ProcessFeedbackStep(RepeatingStep):
    """
    A generic, reusable step to process user feedback on a generated item
    (e.g., audience analysis, knowledge assessment, recommendation).
    """
    def __init__(self, item_name: str, item_key: str, approval_flag: str):
        self.item_name = item_name
        self.item_key = item_key
        super().__init__(approval_flag=approval_flag)

    def execute(self, state: AgentState, llm_service: LanguageModelService, search_service: SearchService) -> tuple[AgentState, str]:
        state["current_step_name"] = f"process_{self.item_key}_feedback"
        user_feedback = state["messages"][-1].content
        modification_count_key = f"{self.item_key}_modification_count"
        modification_count = state.get(modification_count_key, 0)

        if modification_count >= 3:
            state[self.approval_flag] = True # limit loop to 3 iterations, then proceed to the next step
            state['__skip_next_input'] = True # skip asking user for input
            return state, "Ти вичерпав ліміт редагувань на цьому кроці, тому рухаємося далі"

        intent_prompt = f"""
        Користувач дав відгук про {self.item_name}: "{user_feedback}"
        
        Визнач намір користувача з наступних варіантів:
        - CONTINUE: користувач задоволений і хоче продовжити (наприклад: "так", "добре", "згоден", "продовжуємо").
        - MODIFY: хоче виправити, додати або змінити щось конкретне (наприклад: "зміни це", "додай ще", "виправ будь ласка").
        - REGENERATE: хоче, щоб агент перегенерував відповідь повністю (наприклад: "запропонуй інший варіант", "зроби по-новому").
        - UNCLEAR: намір незрозумілий, відгук не стосується теми, або це просто питання. Це варіант за замовчуванням.

        Відповідь лише одним словом: CONTINUE, MODIFY, REGENERATE, або UNCLEAR.
        """
        intent = llm_service.invoke(intent_prompt).strip().upper()

        if intent == "CONTINUE":
            state[self.approval_flag] = True
            state['__skip_next_input'] = True # skip asking user for input
            return state, ""

        if intent == "UNCLEAR":
            clarification_message = (
                "Вибачте, я не зовсім зрозумів ваш відгук. "
                "Будь ласка, уточніть, що саме ви хочете змінити (наприклад, 'додай студентів до аудиторії'), "
                "попросіть 'перегенерувати' відповідь, "
                "або скажіть 'продовжуємо', якщо все гаразд."
            )
            return state, clarification_message

        state[modification_count_key] = modification_count + 1
        current_content = state[self.item_key].get("content", "")

        if intent == "REGENERATE":
            regenerate_prompt = f"Створи НОВИЙ варіант для '{self.item_name}', враховуючи, що попередній варіант був: '{current_content}'. Запропонуй інший підхід."
            new_content = llm_service.invoke(regenerate_prompt)
            state[self.item_key]["content"] = new_content
            return state, f"Ось інший варіант для {self.item_name}:\n\n{new_content}\n\nТепер краще?"
        
        else: 
            modify_prompt = f"""
            Поточний {self.item_name}: '{current_content}'
            Користувач хоче внести зміни: '{user_feedback}'
            Онови {self.item_name}, інтегрувавши зміни від користувача. Поверни лише оновлений текст.
            """
            updated_content = llm_service.invoke(modify_prompt)
            state[self.item_key]["content"] = updated_content
            return state, f"Ось оновлений {self.item_name}:\n\n{updated_content}\n\nЧи потрібні ще якісь зміни?"