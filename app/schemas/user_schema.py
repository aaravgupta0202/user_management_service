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

