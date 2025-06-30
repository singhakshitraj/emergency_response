from pydantic import BaseModel,EmailStr

class sendEmailValidation(BaseModel):
    email:EmailStr
    
class verifyEmailValidation(BaseModel):
    email:str
    otp : str