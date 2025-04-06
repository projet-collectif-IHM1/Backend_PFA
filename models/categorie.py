from pydantic import BaseModel
from typing import List, Optional

class Categorie(BaseModel):
    name: str
    imagecategorie:str