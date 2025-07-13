from fastapi import FastAPI
from models import DialogFlowRequest

app = FastAPI()

@app.post("/webhook/")
async def webhook_handler(body: DialogFlowRequest):
    
    intent_name = body.queryResult.intent.displayName
    product = body.queryResult.parameters["product"]
    
    response_text = f"Got it! You're looking for {product} (Intent: {intent_name})"
    return {"fulfillmentText": response_text}