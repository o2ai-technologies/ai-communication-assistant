from typing import Dict, List, Optional, TypedDict, Annotated
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain.schema import BaseMessage
import operator
from langchain_core.utils.json import parse_json_markdown

# State definition
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    event_info: Dict
    speaker_info: Dict
    analysis_complete: bool
    current_step: str
    audience_analysis: Dict
    final_recommendation: str
    waiting_for_input: bool

class InteractiveSpeakerPrepAgent:
    def __init__(self, gemini_model="gemini-2.0-flash-lite"):
        self.llm = ChatGoogleGenerativeAI(model=gemini_model, temperature=0.7)
        self.search_tool = TavilySearchResults(max_results=5)
        self.state = self._initialize_state()
        self.conversation_steps = [
            "greeting",
            "process_greeting_response",
            "search_event",
            "ask_goal",
            "clarify_goal",
            "ask_stage",
            "analyze_audience",
            "process_audience_feedback",
            "assess_knowledge", 
            "process_knowledge_feedback", 
            "generate_recommendation"
        ]
        self.current_step_index = 0
    
    def _initialize_state(self):
        return {
            "messages": [],
            "event_info": {},
            "speaker_info": {},
            "analysis_complete": False,
            "current_step": "greeting",
            "audience_analysis": {},
            "final_recommendation": "",
            "waiting_for_input": False,
            "audience_approved": False,
            "audience_modification_count": 0,
            "knowledge_approved": False,
            "knowledge_modification_count": 0,
            "knowledge_assessment": {},
        }
        
    def start_conversation(self):
        """Start the interactive conversation"""
        print("🎤 Агент підготовки до виступу")
        print("=" * 50)
        
        # Initial state
        self.state = self._initialize_state()
        self.current_step_index = 0
        
        # Send greeting
        response = self._execute_step("greeting")
        self._display_agent_message(response)
        
        # Start interactive loop
        self._interactive_loop()
    
    def _interactive_loop(self):
        """Main interactive conversation loop"""
        while not self.state["analysis_complete"]:
            try:
                # Get user input
                user_input = input("\n👤 Ви: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'вихід', 'стоп']:
                    print("\n🔚 Розмову завершено. До побачення!")
                    break
                
                if user_input.lower() in ['help', 'допомога']:
                    self._show_help()
                    continue
                
                if not user_input:
                    print("⚠️  Будь ласка, введіть відповідь.")
                    continue
                
                # Process user input
                self._process_user_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\n🔚 Розмову перервано. До побачення!")
                break
            except Exception as e:
                print(f"\n❌ Помилка: {e}")
                print("Спробуйте ще раз або введіть 'help' для допомоги.")
    
    def _process_user_input(self, user_input: str):
        """Process user input and generate next response"""
        # Add user message to state
        self.state["messages"].append(HumanMessage(content=user_input))
        
        current_step_name = None
        if self.current_step_index < len(self.conversation_steps):
            current_step_name = self.conversation_steps[self.current_step_index]
        
        # Special handling for feedback steps
        if current_step_name == "process_audience_feedback":
            # Execute audience feedback processing
            response = self._execute_step("process_audience_feedback")
            
            if response:
                self._display_agent_message(response)
            
            # Check if we should continue or stay in feedback loop
            if not self.state.get("audience_approved", False):
                return  # Stay in the same step for more feedback
            else:
                self.current_step_index += 1  # Move to next step
                
        elif current_step_name == "process_knowledge_feedback":
            # Execute knowledge feedback processing
            response = self._execute_step("process_knowledge_feedback")
            
            if response:
                self._display_agent_message(response)
            
            # Check if we should continue or stay in feedback loop
            if not self.state.get("knowledge_approved", False):
                return  # Stay in the same step for more feedback
            else:
                self.current_step_index += 1  # Move to next step
        else:
            # Normal step progression
            self.current_step_index += 1
        
        # Continue with normal flow
        if self.current_step_index < len(self.conversation_steps):
            current_step = self.conversation_steps[self.current_step_index]
            self.state["current_step"] = current_step
            
            # Execute current step
            response = self._execute_step(current_step)
            
            if response:
                self._display_agent_message(response)
        else:
            # Conversation completed
            self.state["analysis_complete"] = True
            if self.state.get("final_recommendation"):
                print("\n✅ Аналіз завершено!")
                self._show_summary()
            else:
                print("\n👋 До побачення!")


    
    def _execute_step(self, step: str) -> Optional[str]:
        """Execute a conversation step"""
        if step == "greeting":
            return "Привіт! Готуєшся до виступу?"
        
        elif step == "process_greeting_response":
            return self._process_greeting_response()
            
        elif step == "search_event":
            return self._search_event_info()
            
        elif step == "ask_goal":
            return self._ask_goal()
            
        elif step == "clarify_goal":
            return self._clarify_goal()
            
        elif step == "ask_stage":
            return self._ask_stage()
            
        elif step == "analyze_audience":
            return self._analyze_audience()
        
        elif step == "process_audience_feedback":
            return self._process_audience_feedback()
            
        elif step == "assess_knowledge":
            return self._assess_knowledge()
        
        elif step == "process_knowledge_feedback":
            return self._process_knowledge_feedback()
            
        elif step == "generate_recommendation":
            return self._generate_recommendation()
            
        return None
    
    def _process_greeting_response(self) -> Optional[str]:
        """Process user's response to greeting and decide next action"""
        last_message = self.state["messages"][-1]
        user_response = last_message.content.lower().strip()
        
        print("\n🤔 Аналізую вашу відповідь...")
        
        try:
            # Use LLM to analyze the response
            analysis_prompt = f"""
            Користувач відповів на питання "Готуєшся до виступу?": "{user_response}"
            
            Визнач чи це:
            - POSITIVE: користувач готується до виступу (так, готуюся, yes, звичайно, etc.)
            - NEGATIVE: користувач НЕ готується до виступу (ні, не готуюся, no, etc.)  
            - UNCLEAR: відповідь незрозуміла або потребує уточнення
            
            Відповідь лише одним словом: POSITIVE, NEGATIVE, або UNCLEAR
            """
            
            response = self.llm.invoke([HumanMessage(content=analysis_prompt)])
            intent = response.content.strip().upper()
            
            if intent == "POSITIVE":
                return "Класно! Де будеш виступати? На якій конференції чи заході?"
            elif intent == "NEGATIVE":
                return self._handle_negative_response()
            else:  # UNCLEAR
                self.current_step_index -= 1
                return "Вибач, не зовсім зрозумів. Ти готуєшся до якогось виступу чи презентації? (так/ні)"
                
        except Exception as e:
            print(f"⚠️ Помилка аналізу: {e}")
            # Fallback to simple keyword matching
            positive_keywords = ["так", "yes", "готуюся", "готую", "да", "звичайно", "авжеж"]
            negative_keywords = ["ні", "no", "не готуюся", "не готую", "нет"]
            
            if any(keyword in user_response for keyword in positive_keywords):
                return "Класно! Де будеш виступати? На якій конференції чи заході?"
            elif any(keyword in user_response for keyword in negative_keywords):
                return self._handle_negative_response()
            else:
                return "Вибач, не зовсім зрозумів. Ти готуєшся до якогось виступу чи презентації? (так/ні)"

    def _handle_negative_response(self) -> str:
        """Handle when user is not preparing for public speaking"""
        self.state["analysis_complete"] = True
        return """
    Зрозуміло! Якщо в майбутньому будеш готуватися до виступу, презентації чи будь-якого публічного спілкування - звертайся! 

    Я допоможу:
    • Проаналізувати аудиторію
    • Сформулювати ключове повідомлення  
    • Підготувати структуру виступу
    • Дати поради щодо подачі матеріалу

    Удачі! 👋
    """

    
    def _search_event_info(self) -> str:
        """Search for event information"""
        last_message = self.state["messages"][-1]
        event_name = last_message.content
        
        print(f"\n🔍 Шукаю інформацію про {event_name}...")
        
        try:
            # Search for event information
            search_query = f"{event_name} 2025 conference details agenda speakers"
            search_results = self.search_tool.run(search_query)
            
            # Convert search results to string format
            search_text = ""
            if isinstance(search_results, list):
                for result in search_results:
                    if isinstance(result, dict):
                        search_text += f"Title: {result.get('title', '')}\n"
                        search_text += f"Content: {result.get('content', '')}\n"
                        search_text += f"URL: {result.get('url', '')}\n\n"
                    else:
                        search_text += str(result) + "\n\n"
            else:
                search_text = str(search_results)
            
            # Process search results with LLM
            system_prompt = """
            Ти допомагаєш спікеру підготуватися до виступу. 
            Проаналізуй результати пошуку про конференцію і витягни ключову інформацію:
            - Назва події (event_name)
            - Дати проведення (dates)
            - Місце проведення (place)
            - Тематика конференції (theme)
            - Очікувана кількість відвідувачів (attendees)
            - Стейджі/секції якщо є (stages)
            - Цільова аудиторія (target_audience)
            Якщо для поля відсутня інформація - запиши None як значення цього поля.
            
            Поверни результат у JSON форматі.
            """
            
            analysis_prompt = f"Результати пошуку про {event_name}:\n{search_text}"
            
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=analysis_prompt)
            ])
            
            try:
                event_info = parse_json_markdown(response.content)
            except:
                event_info = {
                    "event_name": event_name,
                    "search_results": search_text[:500]
                }
            
            self.state["event_info"] = event_info
            
            # Process search results with LLM to extract and format information
            system_prompt = """
            Ти допомагаєш спікеру підготуватися до виступу. 
            Проаналізуй результати пошуку про конференцію і витягни ключову інформацію.
            
            Сформулюй відповідь українською мовою у природному, дружньому стилі.
            Включи всю знайдену інформацію про:
            - Назву події
            - Дати проведення (якщо знайдено)
            - Місце проведення (якщо знайдено)
            - Тематику конференції
            - Очікувану кількість відвідувачів/учасників (якщо знайдено)
            - Цільову аудиторію (якщо знайдено)
            - Стейджі/секції (якщо є)
            - Інші важливі деталі
            
            Якщо якась інформація не знайдена, не згадуй про неї.
            Заверши повідомлення питанням про тему виступу.
            
            Формат відповіді має бути природним та розмовним, ніби ти розповідаєш другу.
            """
            
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=analysis_prompt)
            ])
            
            return response.content
            
        except Exception as e:
            print(f"⚠️  Помилка при пошуку: {e}")
            return "Не вдалося знайти інформацію про подію. Яка тема твого виступу?"
    
    def _ask_goal(self) -> str:
        """Ask about speaker's goal"""
        last_message = self.state["messages"][-1]
        topic = last_message.content
        
        speaker_info = self.state.get("speaker_info", {})
        speaker_info["topic"] = topic
        self.state["speaker_info"] = speaker_info
        
        return "Чому ти погодився там виступити? Яка твоя мета?"
    
    def _clarify_goal(self) -> str:
        """Clarify and quantify the speaker's goal"""
        last_message = self.state["messages"][-1]
        goal = last_message.content
        
        speaker_info = self.state.get("speaker_info", {})
        speaker_info["goal"] = goal
        self.state["speaker_info"] = speaker_info
        
        try:
            # Generate clarifying question based on goal
            clarification_prompt = f"""
            Спікер хоче: {goal}
            
            Сформулюй питання щоб перевести цю ціль в конкретні критерії досягнення.
            Наприклад, якщо мета "залучити студентів до школи", запитай "скільки студентів має прийти щоб ціль була досягнута?"
            Дай коротку відповідь українською мовою.
            """
            
            response = self.llm.invoke([HumanMessage(content=clarification_prompt)])
            return response.content
            
        except Exception as e:
            return "Як ти будеш розуміти, що мета досягнута? Які конкретні критерії успіху?"
    
    def _ask_stage(self) -> str:
        """Ask about specific stage/track if event has multiple"""
        event_info = self.state.get("event_info", {})
        
        # Check if event has multiple stages/tracks
        event_str = str(event_info).lower()
        if any(word in event_str for word in ["стейдж", "секція", "track", "stage", "потік"]):
            return "На якій секції/стейджі ти будеш виступати?"
        else:
            # Skip to audience analysis directly
            self.current_step_index += 1  # Skip this step
            return self._analyze_audience()
    
    def _analyze_audience(self) -> str:
        """Analyze the audience based on event and topic"""
        event_info = self.state.get("event_info", {})
        speaker_info = self.state.get("speaker_info", {})
        
        print("\n🔍 Аналізую аудиторію...")
        
        try:
            # Search for additional audience information
            search_query = f"{event_info.get('event_name', '')} {speaker_info.get('topic', '')} audience demographics attendees"
            search_results = self.search_tool.run(search_query)
            
            # Convert search results to string format
            search_text = ""
            if isinstance(search_results, list):
                for result in search_results:
                    if isinstance(result, dict):
                        search_text += f"Title: {result.get('title', '')}\n"
                        search_text += f"Content: {result.get('content', '')}\n\n"
                    else:
                        search_text += str(result) + "\n\n"
            else:
                search_text = str(search_results)
            
            # Analyze audience with LLM
            analysis_prompt = f"""
            Проаналізуй аудиторію для виступу:
            
            Конференція: {event_info.get('event_name', 'Невідома')}
            Тема виступу: {speaker_info.get('topic', 'Невідома')}
            Мета спікера: {speaker_info.get('goal', 'Невідома')}
            Додаткова інформація: {search_text[:300]}
            
            Визнач сегменти аудиторії, їх кількість та характеристики. Відповідь українською.
            """
            
            response = self.llm.invoke([HumanMessage(content=analysis_prompt)])
            
            self.state["audience_analysis"] = {"segments": response.content}
            
            # Create confirmation message
            confirmation = f"""
Подивись, чи все вірно:

* Дата проведення: {event_info.get('dates', 'уточнюється')}
* Очікувана кількість глядачів: {event_info.get('attendees', 'уточнюється')}
* Тема: {speaker_info.get('topic')}
* Ціль: {speaker_info.get('goal')}
* Аудиторія: {response.content}

Можливо ще когось додати в сегменти аудиторії?
            """
            
            return confirmation.strip()
            
        except Exception as e:
            return f"Помилка при аналізі аудиторії: {e}. Продовжуємо далі..."
        
    def _process_audience_feedback(self) -> str:
        """Process user feedback about audience segments"""
        last_message = self.state["messages"][-1]
        user_feedback = last_message.content.strip()
        
        print("\n🤔 Аналізую ваш відгук...")
        
        # Prevent infinite loops
        if self.state["audience_modification_count"] >= 3:
            self.state["audience_approved"] = True
            return "Продовжуємо з поточним аналізом аудиторії."
        
        try:
            # Analyze user intent
            intent = self._analyze_user_intent(user_feedback)
            
            if intent == "CONTINUE":
                self.state["audience_approved"] = True
                return "Чудово! Переходимо до наступного етапу."
                
            elif intent == "ADD":
                return self._handle_add_segments(user_feedback)
                
            elif intent == "REMOVE":
                return self._handle_remove_segments(user_feedback)
                
            elif intent == "REWRITE":
                return self._handle_rewrite_segments()
                
            elif intent == "REGENERATE":
                return self._handle_regenerate_segments()
                
            else:
                return self._handle_unclear_feedback()
                
        except Exception as e:
            print(f"⚠️ Помилка обробки відгуку: {e}")
            return "Вибачте, не зрозумів ваш відгук. Чи можете уточнити що ви хочете змінити в аналізі аудиторії?"


    def _analyze_user_intent(self, user_feedback: str) -> str:
        """Analyze what user wants to do with audience segments"""
        intent_prompt = f"""
        Користувач дав відгук про аналіз аудиторії: "{user_feedback}"
        
        Визнач намір користувача:
        - CONTINUE: користувач задоволений і хоче продовжити (так, добре, згоден, продовжуємо, etc.)
        - ADD: хоче додати інформацію (додати, ще є, також, включити, etc.)
        - REMOVE: хоче видалити щось (видалити, прибрати, не потрібно, зайве, etc.)
        - REWRITE: хоче написати сегменти сам (сам напишу, по-своєму, інакше, etc.)
        - REGENERATE: хоче щоб агент перегенерував (заново, по-новому, інший варіант, etc.)
        - UNCLEAR: незрозумілий відгук
        
        Відповідь лише одним словом: CONTINUE, ADD, REMOVE, REWRITE, REGENERATE, або UNCLEAR
        """
        
        response = self.llm.invoke([HumanMessage(content=intent_prompt)])
        return response.content.strip().upper()

    def _handle_add_segments(self, user_feedback: str) -> str:
        """Handle adding information to audience segments"""
        self.state["audience_modification_count"] += 1
        
        current_segments = self.state["audience_analysis"].get("segments", "")
        
        update_prompt = f"""
        Поточний аналіз аудиторії: {current_segments}
        
        Користувач хоче додати: {user_feedback}
        
        Оновіть аналіз аудиторії, включивши нову інформацію від користувача.
        Зберігайте структуру та стиль оригінального аналізу.
        Відповідь українською мовою.
        """
        
        response = self.llm.invoke([HumanMessage(content=update_prompt)])
        updated_segments = response.content
        
        self.state["audience_analysis"]["segments"] = updated_segments
        
        return f"""
    Оновлений аналіз аудиторії:

    {updated_segments}

    Чи потрібні ще якісь зміни?
        """.strip()

    def _handle_remove_segments(self, user_feedback: str) -> str:
        """Handle removing information from audience segments"""
        self.state["audience_modification_count"] += 1
        
        current_segments = self.state["audience_analysis"].get("segments", "")
        
        remove_prompt = f"""
        Поточний аналіз аудиторії: {current_segments}
        
        Користувач хоче видалити/прибрати: {user_feedback}
        
        Оновіть аналіз аудиторії, видаливши зазначену інформацію.
        Зберігайте структуру та стиль оригінального аналізу.
        Відповідь українською мовою.
        """
        
        response = self.llm.invoke([HumanMessage(content=remove_prompt)])
        updated_segments = response.content
        
        self.state["audience_analysis"]["segments"] = updated_segments
        
        return f"""
    Оновлений аналіз аудиторії:

    {updated_segments}

    Чи потрібні ще якісь зміни?
        """.strip()

    def _handle_rewrite_segments(self) -> str:
        """Handle user wanting to write segments themselves"""
        self.state["audience_modification_count"] += 1
        
        return """
    Зрозуміло! Опишіть аудиторію вашого виступу так, як ви її бачите.
    Включіть сегменти, їх характеристики, кількість тощо.
        """.strip()

    def _handle_regenerate_segments(self) -> str:
        """Handle regenerating audience segments"""
        self.state["audience_modification_count"] += 1
        
        print("\n🔄 Генерую новий аналіз аудиторії...")
        
        event_info = self.state.get("event_info", {})
        speaker_info = self.state.get("speaker_info", {})
        
        regenerate_prompt = f"""
        Створіть НОВИЙ аналіз аудиторії для виступу:
        
        Конференція: {event_info.get('event_name', 'Невідома')}
        Тема виступу: {speaker_info.get('topic', 'Невідома')}
        Мета спікера: {speaker_info.get('goal', 'Невідома')}
        
        Використайте інший підхід до сегментації аудиторії.
        Розгляньте різні критерії: досвід, посади, інтереси, мотивація тощо.
        Відповідь українською мовою.
        """
        
        response = self.llm.invoke([HumanMessage(content=regenerate_prompt)])
        new_segments = response.content
        
        self.state["audience_analysis"]["segments"] = new_segments
        
        return f"""
    Новий аналіз аудиторії:

    {new_segments}

    Чи підходить такий варіант?
        """.strip()

    def _handle_unclear_feedback(self) -> str:
        """Handle unclear user feedback"""
        return """
    Не зовсім зрозумів що ви хочете змінити. Ви можете:

    • Додати інформацію: "додай ще студентів"
    • Видалити щось: "прибери частину про..."  
    • Написати самому: "я сам опишу аудиторію"
    • Перегенерувати: "запропонуй інший варіант"
    • Продовжити: "все добре, продовжуємо"

    Що саме ви хочете зробити?
        """.strip()

    
    def _assess_knowledge(self) -> str:
        """Assess what audience currently knows about the topic"""
        speaker_info = self.state.get("speaker_info", {})
        audience_analysis = self.state.get("audience_analysis", {})
        
        print("\n🧠 Оцінюю знання аудиторії...")
        
        try:
            # Generate knowledge assessment
            assessment_prompt = f"""
            Для теми "{speaker_info.get('topic')}" та аудиторії:
            {audience_analysis.get('segments', '')}
            
            Опиши що аудиторія вже зараз знає про цю тему, а що їй треба дізнатися для досягнення мети спікера.
            Відповідь українською мовою, детально та структуровано.
            """
            
            response = self.llm.invoke([HumanMessage(content=assessment_prompt)])
            
            # Store the knowledge assessment
            self.state["knowledge_assessment"] = {"content": response.content}
            
            confirmation = f"""
Для підготовки якісного спіча нам треба зрозуміти що аудиторія вже зараз знає про заявлену тему.

На мою думку зараз аудиторія твого виступу:
{response.content}

Ти згоден з цією оцінкою знань аудиторії?
            """
            
            return confirmation.strip()
            
        except Exception as e:
            return f"Помилка при оцінці знань: {e}. Продовжуємо далі..."
        
    def _process_knowledge_feedback(self) -> str:
        """Process user feedback about knowledge assessment"""
        last_message = self.state["messages"][-1]
        user_feedback = last_message.content.strip()
        
        print("\n🤔 Аналізую ваш відгук про оцінку знань...")
        
        # Prevent infinite loops
        if self.state["knowledge_modification_count"] >= 3:
            self.state["knowledge_approved"] = True
            return "Продовжуємо з поточною оцінкою знань аудиторії."
        
        try:
            # Analyze user intent
            intent = self._analyze_knowledge_intent(user_feedback)
            
            if intent == "AGREE":
                self.current_step_index += 1
                self.state["knowledge_approved"] = True
                return self._generate_recommendation()
                
            elif intent == "ADD_KNOWLEDGE":
                return self._handle_add_knowledge(user_feedback)
                
            elif intent == "REMOVE_KNOWLEDGE":
                return self._handle_remove_knowledge(user_feedback)
                
            elif intent == "CORRECT_KNOWLEDGE":
                return self._handle_correct_knowledge(user_feedback)
                
            elif intent == "REWRITE_KNOWLEDGE":
                return self._handle_rewrite_knowledge()
                
            elif intent == "REGENERATE_KNOWLEDGE":
                return self._handle_regenerate_knowledge()
                
            else:
                return self._handle_unclear_knowledge_feedback()
                
        except Exception as e:
            print(f"⚠️ Помилка обробки відгуку: {e}")
            return "Вибачте, не зрозумів ваш відгук. Чи можете уточнити що ви хочете змінити в оцінці знань аудиторії?"

    def _analyze_knowledge_intent(self, user_feedback: str) -> str:
        """Analyze what user wants to do with knowledge assessment"""
        intent_prompt = f"""
        Користувач дав відгук про оцінку знань аудиторії: "{user_feedback}"
        
        Визнач намір користувача:
        - AGREE: користувач згоден з оцінкою (так, згоден, правильно, точно, etc.)
        - ADD_KNOWLEDGE: хоче додати що аудиторія ще знає (також знають, ще є, додати, etc.)
        - REMOVE_KNOWLEDGE: вважає що щось зайве (не знають, прибрати, видалити, etc.)
        - CORRECT_KNOWLEDGE: хоче виправити неточності (не так, насправді, виправити, etc.)
        - REWRITE_KNOWLEDGE: хоче написати оцінку сам (сам напишу, по-своєму, інакше, etc.)
        - REGENERATE_KNOWLEDGE: хоче щоб агент перегенерував (заново, по-новому, інший варіант, etc.)
        - UNCLEAR: незрозумілий відгук
        
        Відповідь лише одним словом: AGREE, ADD_KNOWLEDGE, REMOVE_KNOWLEDGE, CORRECT_KNOWLEDGE, REWRITE_KNOWLEDGE, REGENERATE_KNOWLEDGE, або UNCLEAR
        """
        
        response = self.llm.invoke([HumanMessage(content=intent_prompt)])
        return response.content.strip().upper()

    def _handle_add_knowledge(self, user_feedback: str) -> str:
        """Handle adding knowledge information"""
        self.state["knowledge_modification_count"] += 1
        
        current_assessment = self.state["knowledge_assessment"].get("content", "")
        
        update_prompt = f"""
        Поточна оцінка знань аудиторії: {current_assessment}
        
        Користувач хоче додати інформацію про знання аудиторії: {user_feedback}
        
        Оновіть оцінку знань, включивши нову інформацію від користувача.
        Зберігайте структуру та стиль оригінальної оцінки.
        Відповідь українською мовою.
        """
        
        response = self.llm.invoke([HumanMessage(content=update_prompt)])
        updated_assessment = response.content
        
        self.state["knowledge_assessment"]["content"] = updated_assessment
        
        return f"""
    Оновлена оцінка знань аудиторії:

    {updated_assessment}

    Чи потрібні ще якісь зміни в оцінці знань?
        """.strip()

    def _handle_remove_knowledge(self, user_feedback: str) -> str:
        """Handle removing knowledge information"""
        self.state["knowledge_modification_count"] += 1
        
        current_assessment = self.state["knowledge_assessment"].get("content", "")
        
        remove_prompt = f"""
        Поточна оцінка знань аудиторії: {current_assessment}
        
        Користувач вважає що треба прибрати/виправити: {user_feedback}
        
        Оновіть оцінку знань, видаливши або виправивши зазначену інформацію.
        Зберігайте структуру та стиль оригінальної оцінки.
        Відповідь українською мовою.
        """
        
        response = self.llm.invoke([HumanMessage(content=remove_prompt)])
        updated_assessment = response.content
        
        self.state["knowledge_assessment"]["content"] = updated_assessment
        
        return f"""
    Оновлена оцінка знань аудиторії:

    {updated_assessment}

    Чи потрібні ще якісь зміни в оцінці знань?
        """.strip()

    def _handle_correct_knowledge(self, user_feedback: str) -> str:
        """Handle correcting knowledge assessment"""
        self.state["knowledge_modification_count"] += 1
        
        current_assessment = self.state["knowledge_assessment"].get("content", "")
        
        correct_prompt = f"""
        Поточна оцінка знань аудиторії: {current_assessment}
        
        Користувач хоче виправити/уточнити: {user_feedback}
        
        Виправте оцінку знань відповідно до зауважень користувача.
        Зберігайте структуру та стиль оригінальної оцінки.
        Відповідь українською мовою.
        """
        
        response = self.llm.invoke([HumanMessage(content=correct_prompt)])
        updated_assessment = response.content
        
        self.state["knowledge_assessment"]["content"] = updated_assessment
        
        return f"""
    Виправлена оцінка знань аудиторії:

    {updated_assessment}

    Тепер все правильно?
        """.strip()

    def _handle_rewrite_knowledge(self) -> str:
        """Handle user wanting to write knowledge assessment themselves"""
        self.state["knowledge_modification_count"] += 1
        
        return """
    Зрозуміло! Опишіть що ваша аудиторія вже знає про тему виступу, а що їй потрібно дізнатися.
    Включіть рівень експертизи, досвід, поточні знання тощо.
        """.strip()

    def _handle_regenerate_knowledge(self) -> str:
        """Handle regenerating knowledge assessment"""
        self.state["knowledge_modification_count"] += 1
        
        print("\n🔄 Генерую нову оцінку знань аудиторії...")
        
        speaker_info = self.state.get("speaker_info", {})
        audience_analysis = self.state.get("audience_analysis", {})
        
        regenerate_prompt = f"""
        Створіть НОВУ оцінку знань аудиторії для виступу:
        
        Тема виступу: {speaker_info.get('topic', 'Невідома')}
        Мета спікера: {speaker_info.get('goal', 'Невідома')}
        Аудиторія: {audience_analysis.get('segments', '')}
        
        Використайте інший підхід до оцінки знань аудиторії.
        Розгляньте різні аспекти: теоретичні знання, практичний досвід, поточні тренди, etc.
        Відповідь українською мовою.
        """
        
        response = self.llm.invoke([HumanMessage(content=regenerate_prompt)])
        new_assessment = response.content
        
        self.state["knowledge_assessment"]["content"] = new_assessment
        
        return f"""
    Нова оцінка знань аудиторії:

    {new_assessment}

    Чи підходить такий варіант оцінки?
        """.strip()

    def _handle_unclear_knowledge_feedback(self) -> str:
        """Handle unclear user feedback about knowledge"""
        return """
    Не зовсім зрозумів що ви хочете змінити в оцінці знань. Ви можете:

    • Додати знання: "аудиторія також знає про..."
    • Прибрати щось: "вони не знають про..."  
    • Виправити: "насправді вони знають..."
    • Написати самому: "я сам опишу їх знання"
    • Перегенерувати: "запропонуй інший варіант"
    • Погодитися: "згоден, все правильно"

    Що саме ви хочете зробити з оцінкою знань?
        """.strip()

    
    def _generate_recommendation(self) -> str:
        """Generate final recommendation for the speaker"""
        speaker_info = self.state.get("speaker_info", {})
        
        print("\n💡 Генерую рекомендації...")
        
        try:
            # Generate main message recommendation
            recommendation_prompt = f"""
            Спікер виступає на тему: {speaker_info.get('topic')}
            Його мета: {speaker_info.get('goal')}
            
            Сформулюй ключову думку, яку аудиторія має винести з виступу для досягнення мети спікера.
            Включи елементи: інноваційність, доступність, приналежність, терміновість.
            Відповідь українською мовою.
            """
            
            response = self.llm.invoke([HumanMessage(content=recommendation_prompt)])
            
            self.state["final_recommendation"] = response.content
            self.state["analysis_complete"] = True
            
            final_message = f"""
Для досягнення твоєї цілі, я вважаю, що аудиторія має винести з виступу наступну основну думку:

"{response.content}"

Згоден?
            """
            
            return final_message.strip()
            
        except Exception as e:
            return f"Помилка при генерації рекомендацій: {e}"
    
    def _display_agent_message(self, message: str):
        """Display agent message with nice formatting"""
        print(f"\n🤖 Агент: {message}")
    
    def _show_help(self):
        """Show help information"""
        help_text = """
📋 Команди:
• help/допомога - показати це меню
• quit/exit/вихід/стоп - завершити розмову

ℹ️  Я допоможу тобі підготуватися до виступу:
1. З'ясуємо деталі події
2. Визначимо твою мету
3. Проаналізуємо аудиторію
4. Дамо рекомендації для презентації
        """
        print(help_text)
    
    def _show_summary(self):
        """Show conversation summary"""
        print("\n" + "="*50)
        print("📊 ПІДСУМОК АНАЛІЗУ")
        print("="*50)
        
        event_info = self.state.get("event_info", {})
        speaker_info = self.state.get("speaker_info", {})
        audience_analysis = self.state.get("audience_analysis", {})
        
        print(f"🎯 Подія: {event_info.get('event_name', 'Невідома')}")
        print(f"📅 Дата: {event_info.get('dates', 'Уточнюється')}")
        print(f"📝 Тема: {speaker_info.get('topic', 'Невідома')}")
        print(f"🎯 Мета: {speaker_info.get('goal', 'Невідома')}")
        print(f"👥 Аудиторія: {len(audience_analysis.get('segments', ''))} символів аналізу")
        print(f"💡 Рекомендація: {self.state.get('final_recommendation', 'Відсутня')[:100]}...")
        
        print("\n✨ Успіхів з виступом!")
    
    def get_current_state(self):
        """Get current conversation state"""
        return self.state.copy()
    
    def reset_conversation(self):
        """Reset conversation to start over"""
        self.state = self._initialize_state()
        self.current_step_index = 0
        print("\n🔄 Розмову скинуто. Почнемо спочатку!")

# Usage example and main interface
def main():
    """Main function to run the interactive agent"""
    print("🚀 Запуск інтерактивного агента підготовки до виступу")
    
    try:
        agent = InteractiveSpeakerPrepAgent()
        agent.start_conversation()
    except Exception as e:
        print(f"❌ Помилка ініціалізації: {e}")
        print("Перевірте налаштування API ключів (GOOGLE_API_KEY, TAVILY_API_KEY) та з'єднання з інтернетом.")

if __name__ == "__main__":
    main()