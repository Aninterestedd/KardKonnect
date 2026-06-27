# KardKonnect 

An AI-powered business card management application that extracts contact information from business cards using Google's Gemini API and provides a clean interface to organize, preview, and manage professional contacts.

## Features

* 📸 Upload business card images
* 🤖 AI-powered OCR using Gemini
* 👤 Automatic extraction of:

  * Name
  * Company
  * Designation
  * Phone Number
  * Email Address
  * Website
  * Address
* 📋 Structured contact preview
* 💾 Stores extracted contacts in a CSV file
* 🌐 Simple Gradio web interface

---

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── contacts.csv
├── .env
└── README.md
```

---

## Prerequisites

* Python 3.10 or later
* A Google Gemini API Key

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Aninterestedd/KardKonnect
cd KardKonnect
```

### 2. Create a virtual environment

```bash
python -m venv card-connect-env
```

### 3. Activate the virtual environment

**Windows**

```bash
card-connect-env\Scripts\activate
```

**macOS / Linux**

```bash
source card-connect-env/bin/activate
```

### 4. Install the required dependencies

```bash
pip install -r requirements.txt
```

---

## Configure the API Key

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Run the Application

Start the Gradio application using:

```bash
python app.py
```

Once the server starts, open the local URL shown in the terminal in your browser.

---

## Usage

1. Launch the application.
2. Upload a business card image.
3. The AI extracts the contact details.
4. Review the extracted information.
5. Save the contact to the CSV database.

---

## Tech Stack

* Python
* Google Gemini API
* Gradio
* Pydantic

---

## Future Improvements

* Contact search and filtering
* Duplicate contact detection
* CRM integration
* Export to Excel or vCard
* Automated follow-up assistant
* Mobile-friendly interface
---
