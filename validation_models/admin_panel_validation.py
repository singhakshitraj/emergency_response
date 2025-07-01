from pydantic import BaseModel
from typing import Optional

class createUserValidation(BaseModel):
    email:str
    role:str
    phone:Optional[str]
    bank_number:str
    department:str
    reporting_manager:Optional[str]
    name:str
    
class deleteUser(BaseModel):
    email:str