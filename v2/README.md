# AI Communication Assistant v2

This is the refactored and enhanced version of the AI-powered interactive agent designed to help speakers prepare for presentations through a conversational interface.

## Project Overview
The v2 tool guides users through a structured conversation to:
- Verify speaker's intention to prepare for public speaking
- Research event information automatically
- Define presentation goals and topics
- Analyze target audience segments
- Assess audience knowledge levels
- Generate personalized recommendations with feedback loops

## Architecture Improvements in V2

### 🏗️ **Modular Design**
- **Service Layer**: Decoupled LLM and search services with dependency injection
- **Step-Based Flow**: Each conversation stage is an independent, reusable step
- **State Management**: Centralized state with proper typing
- **UI Abstraction**: Pluggable user interface system
- **Error Handling**: Improved error handling and graceful degradation

### 📁 **Project Structure**

```
v2/
├── main.py                     # Application entry point
├── src/
│   ├── agent.py               # Main conversation orchestrator
│   ├── config.py              # Configuration settings
│   ├── state.py               # Centralized state management
│   ├── services/              # External service wrappers
│   │   ├── llm_service.py     # Language model service
│   │   └── search_service.py  # Search service wrapper
│   ├── steps/                 # Individual conversation steps
│   │   ├── base_step.py       # Abstract base classes
│   │   ├── greeting.py        # Initial greeting
│   │   ├── search_event.py    # Event information research
│   │   ├── analyze_audience.py # Audience analysis
│   │   ├── assess_knowledge.py # Knowledge assessment
│   │   ├── generate_recommendation.py # Final recommendations
│   │   └── process_feedback.py # Feedback loop handling
│   └── ui/                    # User interface layer
│       ├── base_ui.py         # UI abstraction
│       └── command_line_ui.py # Command line implementation

```

## 🚀 Key Features Implemented:

### 1. **Enhanced Conversation Flow**
- **Modular Steps**: Each conversation stage is a separate, testable class
- **Feedback Loops**: Repeating steps with user approval mechanisms
- **State Persistence**: Centralized state management across all steps
- **Dynamic Flow Control**: Steps can modify conversation flow based on user input

### 2. **Dependency Injection Architecture**
- **Service Abstraction**: LLM and search services are injected dependencies
- **Testability**: Easy to mock services for unit testing
- **Flexibility**: Can swap implementations without changing core logic
- **Maintainability**: Clear separation of concerns

### 3. **Tavily Search Integration**
- Real-time event information gathering
- Automatic extraction of dates, location, attendee count, and themes
- Natural language presentation of search results in Ukrainian
- Structured data storage for internal processing

### 4. **Interactive User Experience**
- Natural Ukrainian language conversation
- Help system with available commands
- Graceful exit handling for non-speakers
- Error handling with user-friendly messages
- Progress indicators and status updates

### 5. **Feedback Loop System**
- **RepeatingStep Pattern**: Steps that require user approval
- **Modification Tracking**: Counts how many times content is modified
- **Approval Flags**: State-based approval system
- **User Control**: Users can request modifications until satisfied

## 🛠️ Installation & Setup:

```bash
# Install dependencies
pip install langchain langchain-google-genai langchain-community tavily-python

# Set environment variables
export GOOGLE_API_KEY="your-gemini-api-key"
export TAVILY_API_KEY="your-tavily-api-key"

# Run CLI version
python main.py
```

## Conversation example:

```bash
🚀 Запуск інтерактивного агента підготовки до виступу

🤖 Агент: Привіт! Готуєшся до виступу?

👤 Ви: так

🤖 Агент: Класно! Де будеш виступати? На якій конференції чи заході?

👤 Ви: Dou Day

🔍 Шукаю інформацію про 'Dou Day' на 2025/2026 рік...

🤖 Агент: Привіт! 👋

Так, я знайшов інформацію про DOU Day ...
Скажіть, будь ласка, на яку тему ви плануєте виступити на DOU Day? Буду радий дізнатися більше! 😊

👤 Ви: що таке квантове машине навчання

🤖 Агент: Чому ти погодився там виступити? Яка твоя мета?

👤 Ви: щоб люди прийшли навчатись в мою літню школу UCU quantum computing

🤖 Агент: Ось декілька питань, щоб конкретизувати ціль залучення людей до літньої школи UCU з квантових обчислень:

*   **Скільки студентів ми хочемо залучити до літньої школи ...

👤 Ви: 10 студентів бакалаврату мають записатися на літню школу

🤖 Агент: Зрозуміло. На якій секції/стейджі ти будеш виступати?

👤 Ви: AI & DataScience Stage

🔍 Аналізую аудиторію...

🤖 Агент: Ось попередній аналіз твоєї аудиторії:

## Аналіз аудиторії DOU Day 2025: "Що таке квантове ...

Чи все вірно, чи хочеш щось додати або змінити? (так/додати/змінити)

👤 Ви: все добре давай далі

🧠 Оцінюю знання аудиторії...

🤖 Агент: Ось оцінка знань аудиторії:

## Що аудиторія DOU Day 2025 вже знає про квантове машинне навчання та що їй потрібно дізнатися ...

Ти згоден з цим?

👤 Ви: так давай далі

💡 Генерую фінальні рекомендації...

🤖 Агент: На основі всього, що ми обговорили, для досягнення твоєї цілі я вважаю, що ключова думка, яку аудиторія має винести з виступу, повинна бути такою: ...

Чи згоден ти з цією основною рекомендацією? Можливо, хочеш щось змінити або доповнити?

👤 Ви: так чудово

==================================================
📊 ПІДСУМОК АНАЛІЗУ
==================================================
✨ Подія: DOU Day 2025
📅 Дата: May 16–17, 2025
📍 Місце: Kyiv
🫂 Учасники: 2,500+
📝 Тема: що таке квантове машине навчання
🎯 Мета: щоб люди прийшли навчатись в мою літню школу UCU quantum computing
💡 Рекомендація: Квантове машинне навчання – це не майбутнє, а інструмент, який вже зараз відкриває нові можливості для вирішення складних задач. Приєднуйтесь до літньої школи UCU quantum computing, щоб стати піонерами цієї революційної галузі та отримати конкурентну перевагу вже сьогодні!

✨ Успіхів з виступом!
```

## 🔧 Configuration

The application uses Google Gemma 3 27B IT model by default. You can modify the model in `src/config.py`:

```
LLM_MODEL_NAME = "models/gemma-3-27b-it"
```

## 🏛️ Architecture Patterns

### Step Pattern

Each conversation step implements the `ConversationStep` interface:

```
class ConversationStep(ABC):
    def execute(self, state, llm_service, search_service) -> tuple[AgentState, str]:
        pass
```

### Repeating Step Pattern

For steps requiring user feedback:

```
class RepeatingStep(ConversationStep):
    def __init__(self, approval_flag: str):
        self.approval_flag = approval_flag
```

### Service Layer

Services are injected into the agent for better testability:

```
agent = InteractiveSpeakerPrepAgent(
    llm_service=llm_service,
    search_service=search_service,
    ui=ui
)
```
