from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.environ['GEMINI_API_KEY']
print(api_key)