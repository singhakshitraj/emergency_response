from pydantic import BaseModel
    
class addOrDeleteContactsValidation(BaseModel):
    name : str
    department : str
    employee_type : str
