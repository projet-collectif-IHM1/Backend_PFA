from pydantic import BaseModel
from typing import List, Optional

class But(BaseModel):
   but:str
   user_id:str