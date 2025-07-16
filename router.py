from models import DialogFlowRequest
from handlers.books_handler import books_handler
from handlers.laptops_handler import laptops_handler

def handle_intent(body: DialogFlowRequest):
    
    intent = body.queryResult.intent.displayName
    
    match intent:
        case "SearchBooks":
            return books_handler(body)
        case "SearchLaptops":
            return laptops_handler(body)
        case _:
            return {"fulfillmentText": "Sorry, I didn't understand your request."}
    
    
