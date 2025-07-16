from fastapi import FastAPI
from models import DialogFlowRequest
from router import handle_intent

app = FastAPI()

@app.post("/webhook/")
async def webhook_handler(body: DialogFlowRequest):
    return handle_intent(body)
