import os
from dotenv import load_dotenv
from google.genai import Client
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)

load_dotenv()

if os.getenv("GOOGLE_API_KEY") is None:
    raise ValueError("GOOGLE_API_KEY is not set")

# Used for Google Search API
genai_client = Client(api_key=os.getenv("GOOGLE_API_KEY"))
