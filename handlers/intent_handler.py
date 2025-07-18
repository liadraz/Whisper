from models.dialogflow_request import DialogFlowRequest
from handlers.books_handler import books_handler
from handlers.laptops_handler import laptops_handler

def handle_intent(body: DialogFlowRequest):
    
    intent = body.queryResult.intent.displayName
    
    match intent:
        case "SearchBooks":
            message = books_handler(body)
        case "SearchLaptops":
            message = laptops_handler(body)
        case _:
            message = "Sorry, I didn't understand your request."
    
    return { "fulfillmentText": message }
    
