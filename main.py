import os
from agents.pdf_agent import process_pdf
from classifier import classify_input
from tone_agent import detect_tone
from urgency_agent import detect_urgency
from action_router import trigger_action

def route_input(file_path):
    content = process_pdf("C:\Users\Anusha singh\OneDrive\Desktop\classifier_agent\sample_inputs\sample_invoice.pdf")
    classification_result = classify_input("C:\Users\Anusha singh\OneDrive\Desktop\classifier_agent\sample_inputs\sample_invoice.pdf")
    classification = classification_result["intent"]
    tone = detect_tone(content)
    urgency = detect_urgency(content)

    result = {
        "classification": classification,
        "tone": tone,
        "urgency": urgency,
    }

    action_type = "create_ticket"
    if urgency == "high" or tone == "angry":
        action_type = "escalate_issue"
    elif classification == "compliance":
        action_type = "flag_compliance_risk"

    payload = {
        "email_content": content,
        "classification": classification,
        "tone": tone,
        "urgency": urgency,
    }
    action_result = trigger_action(action_type, payload)
    result["action"] = action_type
    result["action_result"] = action_result
    return result

from flask import Flask, request, render_template
from main import route_input
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        result = route_input(filepath)
        return render_template("result.html", result=result)
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
