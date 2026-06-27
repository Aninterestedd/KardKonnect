from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from PIL import Image
import os

load_dotenv()
gemini_api_key = os.environ["GEMINI_API_KEY"]

# Pydantic Model
class ContactCard(BaseModel):
    name: str = Field(description="Full name of the person")
    company_name: str = Field(description="Company the person works at")
    phone_number: str = Field(description="Phone number with country code if available")
    email: str = Field(description="Email address")

# Image preprocess function
def preprocess_image(image):
    image = image.convert("RGB")
    image.thumbnail((1024, 1024))
    return image

# Load image (same format as Gradio will give)
image = Image.open("test-dataset/1.jpeg")
image = preprocess_image(image)


prompt = """
Extract contact details from this business card image.

Return ONLY valid JSON in this format:
{
  "name": "",
  "company_name": "",
  "phone_number": "",
  "email": ""
}

Rules:
- Do not include extra text
- If a field is missing, return empty string
- Normalize phone number with country code if possible
"""

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=[image, prompt],
    config={
        "response_mime_type": "application/json",
        "response_json_schema": ContactCard.model_json_schema(),
    },
)

contact = ContactCard.model_validate_json(response.text)

print(contact)