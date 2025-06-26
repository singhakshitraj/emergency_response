from pydantic import BaseModel

class checkAdminOrUserValidation(BaseModel):
    email:str