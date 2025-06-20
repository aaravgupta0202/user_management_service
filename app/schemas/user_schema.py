from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
    profile_image: Optional[str] = None
    mobile_no : Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None    
    
    class Config():
        orm_mode = True

class UserFormData(BaseModel):
    name: str
    surname: str
    email : str
    password : str
    profile_image: str
    mobile_no : int
    city: str
    state: str
    country: str    
    
    class Config():
        orm_mode = True

