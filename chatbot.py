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
            "assess_knowledge", 
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
            "waiting_for_input": False
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
        
        # Move to next step
        self.current_step_index += 1
        
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
            if self.state.get("final_recommendation"):  # Only show summary if we completed full analysis
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
            
        elif step == "assess_knowledge":
            return self._assess_knowledge()
            
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
            - Дати проведення
            - Місце проведення  
            - Тематика конференції
            - Очікувана кількість відвідувачів
            - Стейджі/секції якщо є
            - Цільова аудиторія
            
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
            
            #Create response message
            time_info = ""
            if "дата" in str(event_info).lower() or "date" in str(event_info).lower():
                time_info = "Я бачу що в тебе є час на підготовку. "
            
            return f"{response.content}\n\n{time_info}Тепер розкажи, яка тема твого виступу?"
            
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
            
            confirmation = f"""
Для підготовки якісного спіча нам треба зрозуміти що аудиторія вже зараз знає про заявлену тему.

На мою думку зараз аудиторія твого виступу:
{response.content}

Ти згоден?
            """
            
            return confirmation.strip()
            
        except Exception as e:
            return f"Помилка при оцінці знань: {e}. Продовжуємо далі..."
    
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