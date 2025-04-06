from pydantic import BaseModel
from typing import List, Optional

class BackGround(BaseModel):
    video: str
    imageBG:str
    categorie_id: str
