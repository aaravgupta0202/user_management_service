from pydantic import BaseModel
from typing import Optional

class ResponseSchema(BaseModel):
    status: bool = True
    response: str
    data: Optional[dict | list] = None
