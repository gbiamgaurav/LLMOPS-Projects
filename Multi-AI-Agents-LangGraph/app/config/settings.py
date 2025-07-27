
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    ALLOWED_MODEL_NAMES = [
        "llama-3.3-70b-versatile",
        "deepseek-r1-distill-llama-70b",
        "gemma2-9b-it",
    ]


settings = Settings()