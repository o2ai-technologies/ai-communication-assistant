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

### Orchestration

It is responsibility of agent.py file

```
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
```
