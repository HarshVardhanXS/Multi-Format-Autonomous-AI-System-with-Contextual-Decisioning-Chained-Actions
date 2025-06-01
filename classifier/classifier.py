import mimetypes
import os
from datetime import datetime
from transformers import pipeline
from memory.memory_store import write_to_memory

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

INTENT_LABELS = ["RFQ", "Complaint", "Invoice", "Regulation", "Fraud Risk"]

def detect_format(file_path):
    mime, _ = mimetypes.guess_type(file_path)
    if mime == 'application/pdf':
        return 'PDF'
    elif mime == 'application/json':
        return 'JSON'
    elif mime in ['text/plain', 'message/rfc822']:
        return 'Email'
    return 'Unknown'

def read_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ""

def classify_input(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    if "invoice" in content:
        intent = "Invoice"
    elif "complain" in content or "disappointed" in content:
        intent = "Complaint"
    elif "gdpr" in content or "fda" in content:
        intent = "Regulation"
    elif "fraud" in content:
        intent = "Fraud Risk"
    elif "quote" in content or "price" in content:
        intent = "RFQ"
    else:
        intent = "Unknown"

    return {
        "format": "Email" if "from:" in content else "Unknown",
        "intent": intent,
        "route_to": "email_agent" if "from:" in content else None
    }

