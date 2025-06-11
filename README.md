# AI Communication Assistant

This project is an AI-powered interactive agent designed to help speakers prepare for presentations through a conversational interface.

## Project Overview
The tool guides users through a structured conversation to:
- Verify speaker's intention to prepare for public speaking
- Research event information automatically
- Define presentation goals and topics
- Analyze target audience segments
- Assess audience knowledge levels
- Generate personalized recommendations

## Architecture
- Interactive conversational agent with step-by-step flow
- Utilizes LangChain framework with Google Gemini integration
- Employs Tavily search for real-time event information gathering
- Ukrainian language interface with natural conversation flow
- State-based conversation management

## 🚀 Key Features Implemented:

### 1. **Google Gemini Integration**
- Uses `ChatGoogleGenerativeAI` with Gemini 2.0 Flash Lite
- Intelligent response analysis and intent detection
- Temperature set to 0.7 for natural conversational responses
- JSON parsing with fallback handling

### 2. **Smart Conversation Flow**
- **Greeting & Intent Verification**: Confirms user's intention to prepare for speaking
- **Event Information Research**: Automatically searches and presents event details
- **Goal Definition**: Helps clarify speaker's objectives and success criteria
- **Audience Analysis**: Identifies and analyzes target audience segments
- **Knowledge Assessment**: Evaluates what audience already knows
- **Recommendation Generation**: Creates personalized speaking recommendations

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

### 5. **Chainlit Web Interface**
- Modern web-based chat interface
- Real-time message updates
- Improved user experience over console-based interaction
- Persistent chat history during session
- Emoji support for better visual communication

## 🛠️ Installation & Setup:

```bash
# Install dependencies
pip install langchain langchain-google-genai langchain-community langgraph tavily-python chainlit

# Set environment variables
export GOOGLE_API_KEY="your-gemini-api-key"
export TAVILY_API_KEY="your-tavily-api-key"

# Run the console application
python chatbot.py

# OR run the web interface with Chainlit
chainlit run chainlit_demo_app.py
```
