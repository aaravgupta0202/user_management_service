from typing import Optional
from pydantic import BaseModel

class UserSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
    profile_image: Optional[str] = None
    mobile_no : Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    is_picture_remove: Optional[int] = 0  
    
    class Config():
        orm_mode = True
