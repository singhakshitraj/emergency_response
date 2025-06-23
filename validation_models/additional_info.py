from pydantic import BaseModel

class addAdditionalInfoValidation(BaseModel):
    name : str
    content : str

class deleteAdditionalInfoValidation(BaseModel):
    id : str