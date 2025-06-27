from typing import Optional
from pydantic import BaseModel

class SubmitResetSchema(BaseModel):
    email : str = None
    
class VerifyOTPSchema(BaseModel):
    email : str = None
    otp : str = None

class ChangePasswordSchema(BaseModel):
    email : str = None
    password : str = None