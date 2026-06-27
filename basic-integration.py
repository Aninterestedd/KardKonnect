import gradio as gr
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
from PIL import Image
from datetime import datetime
import os
import re
import pandas as pd

load_dotenv()
client = genai.Client()

CSV_FILE = "contacts.csv"


# Schema
class ContactCard(BaseModel):
    name: str
    company_name: str
    phone_number: str
    email: str


# Preprocess
def preprocess_image(image):
    image = image.convert("RGB")
    image.thumbnail((1024, 1024))
    return image


# Phone formatter
def format_phone(phone):
    if not phone or type(phone) != str:
        return ""

    digits = re.sub(r"\D", "", phone)

    if digits.startswith("0"):
        digits = digits[1:]

    if len(digits) == 10:
        digits = "91" + digits

    return digits


# Load existing contacts
def load_contacts():
    if not os.path.exists(CSV_FILE):
        return []
    df = pd.read_csv(CSV_FILE)
    return df.to_dict(orient="records")


# Save contact
def save_contact(contact):
    df_new = pd.DataFrame([contact])

    if os.path.exists(CSV_FILE):
        df_existing = pd.read_csv(CSV_FILE)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(CSV_FILE, index=False)


# Gemini extraction
def extract_contact(image):
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
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[image, prompt],
        config={
            "response_mime_type": "application/json",
            "response_json_schema": ContactCard.model_json_schema(),
        },
    )

    data = ContactCard.model_validate_json(response.text).dict()

    data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return data


# Add contact (write to CSV)
def add_contact(image):
    if image is None:
        return load_contacts()

    new_contact = extract_contact(image)
    save_contact(new_contact)

    return load_contacts()  # reload from file


with gr.Blocks() as demo:

    contacts_state = gr.State(load_contacts())  # initial load

    image_input = gr.Image(
        sources=["upload", "webcam"],
        type="pil",
        height=200,
        width=500,
        label="Scan Business Card"
    )

    image_input.change(
        fn=add_contact,
        inputs=image_input,
        outputs=contacts_state
    )

    @gr.render()
    def show_contacts():

        contacts = load_contacts()
        
        if not contacts:
            gr.Markdown("No contacts yet. Scan a card to begin.")
        else:
            gr.Markdown("## Saved Contacts")

            for contact in contacts:
                phone = format_phone(contact["phone_number"])
                wa_link = f"https://wa.me/{phone}"

                gr.HTML(f"""
                <div style="
                    padding: 16px;
                    margin-bottom: 12px;
                    border-radius: 12px;
                    border: 1px solid #e5e7eb;
                    background-color: #000000;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                ">
                    <h3 style="margin: 0 0 8px 0;">{contact['name']}</h3>
                    
                    <p><strong>Company:</strong> {contact['company_name']}</p>

                    <p>
                    <strong>Phone:</strong> 
                    <a href="tel:{format_phone(contact['phone_number'])}" style="color:#4da6ff; text-decoration:none;">
                        {contact['phone_number']}
                    </a>
                    </p>

                    <p>
                    <strong>Email:</strong> 
                    <a href="mailto:{contact['email']}" style="color:#4da6ff; text-decoration:none;">
                        {contact['email']}
                    </a>
                    </p>

                    <p><strong>Added:</strong> {contact['created_at']}</p>

                    <button 
                        onclick="window.open('https://wa.me/{format_phone(contact['phone_number'])}', '_blank')"
                        style="
                            margin-top: 12px;
                            padding: 8px 14px;
                            border-radius: 8px;
                            border: none;
                            background-color: #25D366;
                            color: white;
                            font-weight: 600;
                            cursor: pointer;
                        "
                    >
                        WhatsApp
                    </button>

                </div>
                """)


demo.launch(share=True)