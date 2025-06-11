# src/ui/command_line_ui.py
from src.ui.base_ui import BaseUI
from src.state import AgentState

class CommandLineUI(BaseUI):
    """Implementation of the UI for the command line."""
    def display_agent_message(self, message: str):
        print(f"\n🤖 Агент: {message}")

    def get_user_input(self) -> str:
        return input("\n👤 Ви: ").strip()

    def show_summary(self, state: AgentState):
        print("\n" + "="*50)
        print("📊 ПІДСУМОК АНАЛІЗУ")
        print("="*50)
        event_info = state.get("event_info", {})
        speaker_info = state.get("speaker_info", {})
        print(f"✨ Подія: {event_info.get('event_name', 'Невідомо')}")
        print(f"📅 Дата: {event_info.get('dates', 'Уточнюється')}")
        print(f"📍 Місце: {event_info.get('place', 'Невідомо')}")
        print(f"🫂 Учасники: {event_info.get('attendees', 'Невідомо')}")
        print(f"📝 Тема: {speaker_info.get('topic', 'Невідомо')}")
        print(f"🎯 Мета: {speaker_info.get('goal', 'Невідомо')}")
        print(f"💡 Рекомендація: {state.get('final_recommendation', {"content": 'Відсутня'}).get('content')}")
        print("\n✨ Успіхів з виступом!")

    def show_help(self):
        help_text = """
📋 Команди:
• help/допомога - показати це меню
• quit/exit/вихід/стоп - завершити розмову
        """
        print(help_text)