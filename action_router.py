import requests
import time
from flask import Flask, request, render_template, redirect, url_for
from main import route_input

def trigger_action(action_type: str, payload: dict, retries: int = 3, delay: float = 2.0):
    endpoints = {
        "create_ticket": "https://example.com/api/crm/tickets",
        "escalate_issue": "https://example.com/api/escalations",
        "flag_compliance_risk": "https://example.com/api/risk_alerts"
    }
    url = endpoints.get(action_type)
    if not url:
        raise ValueError(f"Unknown action type: {action_type}")

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return {"status": "success", "response": response.json()}
        except Exception as e:
            if attempt == retries:
                return {"status": "error", "error": str(e), "attempts": attempt}
            time.sleep(delay)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filepath = f"uploads/{file.filename}"
        file.save(filepath)
        result = route_input(filepath)
        return render_template("result.html", result=result)
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
