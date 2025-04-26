from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    FamilyName:str
    password: str
    education: Optional[str] = None
    country: Optional[str] = None

    