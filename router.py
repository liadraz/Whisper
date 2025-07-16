from models import DialogFlowRequest
import handlers

def handle_intent(body: DialogFlowRequest):
    
    intent = body.queryResult.intent.displayName
    
    match intent:
        case "SearchBooks":
            return books_handler(body)
        case "SearchLaptops":
            return laptops_handler(body)
        case _:
            return {"fulfillmentText": "Sorry, I didn't understand your request."}
    
    
