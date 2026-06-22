import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def analyze_text(text: str) -> dict:
    prompt = f"""
You are a cybercrime detection AI for India's law enforcement. Analyze the following message/text for fraud indicators.

Text to analyze:
\"\"\"{text}\"\"\"

Respond ONLY in this exact JSON format, nothing else:
{{
  "risk_score": <integer 0-100>,
  "is_scam": <true or false>,
  "scam_type": "<type of scam or 'Not a scam'>",
  "detected_patterns": ["<pattern1>", "<pattern2>"],
  "risk_level": "<Low / Medium / High / Critical>",
  "explanation": "<2-3 sentence explanation>",
  "recommended_actions": ["<action1>", "<action2>", "<action3>"]
}}

Common Indian scam types to detect:
- Digital Arrest Scam
- KYC Expiry Scam
- Fake Job Offer
- Lottery/Prize Scam
- UPI Refund Scam
- Bank Account Freeze Scam
- Authority Impersonation (CBI/ED/Police)
- Electricity Disconnection Scam
- FedEx/Courier Parcel Scam
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)


def analyze_image(image_bytes: bytes, mime_type: str = "image/png") -> dict:
    prompt = """
You are a cybercrime detection AI for India's law enforcement. Analyze this screenshot for fraud indicators.

Respond ONLY in this exact JSON format, nothing else:
{
  "risk_score": <integer 0-100>,
  "is_scam": <true or false>,
  "scam_type": "<type of scam or 'Not a scam'>",
  "detected_patterns": ["<pattern1>", "<pattern2>"],
  "risk_level": "<Low / Medium / High / Critical>",
  "explanation": "<2-3 sentence explanation>",
  "recommended_actions": ["<action1>", "<action2>", "<action3>"]
}
"""
    image_part = {"mime_type": mime_type, "data": image_bytes}
    response = model.generate_content([prompt, image_part])
    raw = response.text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)