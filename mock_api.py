from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/crm/escalate")
async def escalate_crm(data: Request):
    body = await data.json()
    print("🔥 CRM Escalation Received:", body)
    return {"status": "escalated", "details": body}

@app.post("/log")
async def log_routine(data: Request):
    body = await data.json()
    print("📝 Routine Log Received:", body)
    return {"status": "logged", "details": body}
