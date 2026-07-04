from groq import Groq
import os
from dotenv import load_dotenv
import json
import re
import base64

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_text(text: str) -> dict:
    prompt = f"""
You are a cybercrime detection AI for India's law enforcement.

Analyze the following message/text for fraud indicators.

Text:
{text}

Respond ONLY in valid JSON:

{{
  "risk_score": 0,
  "is_scam": false,
  "scam_type": "",
  "detected_patterns": [],
  "risk_level": "",
  "explanation": "",
  "recommended_actions": []
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    return json.loads(raw)


def analyze_image(image_bytes: bytes, mime_type: str = "image/png") -> dict:

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
You are a cybercrime detection AI for India's law enforcement.

Analyze this screenshot for fraud indicators.

Respond ONLY in valid JSON:

{
  "risk_score": 0,
  "is_scam": false,
  "scam_type": "",
  "detected_patterns": [],
  "risk_level": "",
  "explanation": "",
  "recommended_actions": []
}
"""

    response = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    return json.loads(raw)