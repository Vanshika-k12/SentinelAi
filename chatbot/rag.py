from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are SentinelAI Law Enforcement Copilot.

You help Indian police officers and cybercrime investigators.

You assist with:
- Digital Arrest Scams
- UPI Fraud
- KYC Scams
- Job Frauds
- Cybercrime Investigation
- Fraud Pattern Analysis
- NCRP Reporting

Provide professional and structured responses.
"""


def get_copilot_response(user_message: str, chat_history: list) -> str:

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for msg in chat_history:
        messages.append({
            "role": "assistant" if msg["role"] == "assistant" else "user",
            "content": msg["content"]
        })

    messages.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content