from fastapi import APIRouter

from models.dialogflow_request import DialogFlowRequest
from handlers.intent_handler import handle_intent

router = APIRouter()

@router.post("/webhook/")
async def webhook_handler(body: DialogFlowRequest):
    return handle_intent(body)
