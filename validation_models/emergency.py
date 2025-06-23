from pydantic import BaseModel

class addEmergencyValidation(BaseModel):
    location:str
    type:str
    additional_info:str
    
class emergencyResolvedValidation(BaseModel):
    id:int