# main.py
from src.agent import InteractiveSpeakerPrepAgent
from src.services.llm_service import LanguageModelService
from src.services.search_service import SearchService
from src.ui.command_line_ui import CommandLineUI
from src.config import LLM_MODEL_NAME

def main():
    """Main function to initialize and run the interactive agent."""
    print("🚀 Запуск інтерактивного агента підготовки до виступу")

    try:
        # 1. Initialize services (external dependencies)
        llm_service = LanguageModelService(model_name=LLM_MODEL_NAME)
        search_service = SearchService(max_results=5)

        # 2. Initialize the user interface
        ui = CommandLineUI()

        # 3. Initialize the agent and inject its dependencies
        agent = InteractiveSpeakerPrepAgent(
            llm_service=llm_service,
            search_service=search_service,
            ui=ui
        )

        # 4. Start the conversation
        agent.run()
                
    except KeyboardInterrupt:
        print("\n\n🔚 Розмову перервано. До побачення!")

    except Exception as e:
        print(f"❌ Помилка ініціалізації: {e}")
        print("Перевірте налаштування API ключів (GOOGLE_API_KEY, TAVILY_API_KEY) та з'єднання з інтернетом.")

if __name__ == "__main__":
    main()