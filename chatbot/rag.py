import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    system_instruction="""
You are SentinelAI Law Enforcement Copilot — an AI assistant for Indian police officers, 
CBI agents, and cybercrime investigators. You help analyze fraud patterns, 
generate investigation reports, and provide intelligence summaries.

You have access to India's cybercrime data including:
- 1.14 million cybercrime complaints in 2023
- Digital arrest scams defrauded Rs 1,776 crore in first 9 months of 2024
- Top fraud hotspots: Delhi NCR, Mumbai, Bangalore
- Common scam types: Digital Arrest, KYC Scam, UPI Fraud, Job Fraud, FedEx Courier Scam

Always respond professionally. When asked to generate reports, format them clearly.
When asked about scam clusters or patterns, provide specific data-driven insights.
Always recommend NCRP (National Cyber Crime Reporting Portal) reporting for victims.
"""
)

def get_copilot_response(user_message: str, chat_history: list) -> str:
    # Build conversation history for Gemini
    history = []
    for msg in chat_history:
        history.append({"role": msg["role"], "parts": [msg["content"]]})

    chat = model.start_chat(history=history)
    response = chat.send_message(user_message)
    return response.text