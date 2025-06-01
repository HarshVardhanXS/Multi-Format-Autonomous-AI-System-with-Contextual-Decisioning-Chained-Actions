import os
from datetime import datetime

def detect_tone(text):

    if "urgent" in text.lower() or "immediately" in text.lower():
        return "angry"
    if "please" in text.lower():
        return "polite"
    return "neutral"

def detect_urgency(text):
    if "urgent" in text.lower() or "immediately" in text.lower():
        return "high"
    return "normal"

def extract_email_fields(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    sender = "unknown@example.com"

    issue = "Complaint about service delay" if "complaint" in content.lower() else "General inquiry"

    tone = detect_tone(content)
    urgency = detect_urgency(content)

    return {
        "source": file_path,
        "timestamp": str(datetime.now()),
        "sender": sender,
        "issue": issue,
        "tone": tone,
        "urgency": urgency,
        "raw_text": content
    }

def process_email(file_path, memory=None):
    email_data = extract_email_fields(file_path)

    if memory:
        memory.update_memory({"email_agent_output": email_data})

    return email_data
