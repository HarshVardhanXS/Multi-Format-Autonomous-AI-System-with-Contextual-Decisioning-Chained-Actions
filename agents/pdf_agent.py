import fitz  # PyMuPDF
import re
from datetime import datetime

SENSITIVE_TERMS = ["GDPR", "HIPAA", "CCPA", "FDA", "SOC 2", "ITAR", "FERPA"]

def extract_text_from_pdf(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return ""

def extract_total_amount(text):

    match = re.search(r"Total\s*Amount[:\s]*\$?([\d,]+\.\d{2})", text, re.IGNORECASE)
    if not match:
        match = re.search(r"Total[:\s]*\$?([\d,]+\.\d{2})", text, re.IGNORECASE)
    if match:
        amt_str = match.group(1).replace(",", "")
        try:
            return float(amt_str)
        except ValueError:
            return 0.0
    return 0.0

def detect_sensitive_terms(text):
    found = [term for term in SENSITIVE_TERMS if term.lower() in text.lower()]
    return found

def extract_line_items(text):

    lines = text.splitlines()
    items = []
    item_pattern = re.compile(r"(.+?)\s+(\d+)\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})")
    
    for line in lines:
        match = item_pattern.match(line.strip())
        if match:
            desc = match.group(1).strip()
            qty = int(match.group(2))
            unit_price = float(match.group(3).replace(",", ""))
            total = float(match.group(4).replace(",", ""))
            items.append({
                "description": desc,
                "qty": qty,
                "unit_price": unit_price,
                "total": total
            })
    return items

def process_pdf(file_path):
    timestamp = str(datetime.now())
    text = extract_text_from_pdf(file_path)

    total_amount = extract_total_amount(text)
    sensitive_terms = detect_sensitive_terms(text)
    line_items = extract_line_items(text)

    anomalies = []
    if total_amount > 10000:
        anomalies.append("High invoice total")
    if sensitive_terms:
        anomalies.append("Sensitive policy content detected")

    result = {
        "source": file_path,
        "timestamp": timestamp,
        "status": "valid",
        "anomalies": anomalies,
        "data": {
            "total_amount": total_amount,
            "sensitive_terms": sensitive_terms,
            "line_items": line_items,
            "text_snippet": text[:500] + "..." if len(text) > 500 else text
        }
    }

    print("\n📩 PDF Agent Output:")
    for k, v in result.items():
        print(f"{k}: {v}")

    if anomalies:
        print("\n⚠️ Anomalies detected!")
    else:
        print("\n✅ No anomalies detected.")
    
    return result
