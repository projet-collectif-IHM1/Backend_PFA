from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str
    education:str
    country_id:str
    role: str = "user"