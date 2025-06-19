import os
from dotenv import load_dotenv
from google.genai import Client
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)

from langchain_openai import ChatOpenAI

load_dotenv()
# if os.getenv("OPENROUTER_API_KEY") is None:
#     raise ValueError("OPENROUTER_API_KEY is not set")

# # --- Configure the LLM to use the OpenRouter API ---
# llm = ChatOpenAI(
#     # 1. Set the model name to the one you want from OpenRouter
#     model="google/gemini-2.0-flash-001", 
    
#     # 2. Get the API key from the environment variable
#     api_key=os.getenv("OPENROUTER_API_KEY"),
    
#     # 3. Set the base URL to OpenRouter's endpoint
#     base_url="https://openrouter.ai/api/v1",
    
#     # 4. Set the mandatory HTTP-Referer header
#     # Replace "YOUR_APP_NAME" with the name of your app or project URL
#     default_headers={
#         "HTTP-Referer": "http://localhost:8000", # Or your app's URL
#         "X-Title": "AI communication agent",
#     }
# )

if os.getenv("GOOGLE_API_KEY") is None:
    raise ValueError("GOOGLE_API_KEY is not set")

# Used for Google Search API
genai_client = Client(api_key=os.getenv("GOOGLE_API_KEY"))
