from pydantic import BaseModel
from typing import Dict


class IntentInfo(BaseModel):
    displayName: str

class QueryResult(BaseModel):
    intent: IntentInfo
    parameters: Dict[str, str]
    
class DialogFlowRequest(BaseModel):
    queryResult: QueryResult
    
    

#  DialogFlow model webhook request
# {
#   "queryResult": {
#     "intent": {
#       "displayName": "SearchProduct"
#     },
#     "parameters": {
#       "product": "laptop"
#     }
#   }
# }
