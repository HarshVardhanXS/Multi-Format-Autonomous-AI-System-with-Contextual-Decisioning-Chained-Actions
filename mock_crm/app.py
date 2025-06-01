from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Mock CRM API", version="0.1.0")

class EscalateRequest(BaseModel):
    source: str
    timestamp: str
    sender: str
    urgency: str
    tone: str
    action_taken: str

@app.post("/crm/escalate")
async def escalate(data: EscalateRequest):

    return {"message": f"Escalation logged for {data.source}"}
