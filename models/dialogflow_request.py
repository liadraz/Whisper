from pydantic import BaseModel
from typing import Dict


class IntentInfo(BaseModel):
    displayName: str

class QueryResult(BaseModel):
    intent: IntentInfo
    parameters: Dict[str, str]
    
class DialogFlowRequest(BaseModel):
    queryResult: QueryResult
    
    
#
# Sample Dialogflow webhook request body:
#
# {
#   "queryResult": {
#     "intent": {
#       "displayName": "SearchProduct"
#     },
#     "parameters": {
#       "product": "laptop",
#       "price": 40
#     }
#   }
# }
#
# Explanation:
# - "displayName": name of the matched intent.
# - "parameters": extracted entities from the user's input.
#     - "product": the item the user is interested in.
#     - "price": price limit or budget specified by the user.