from pydantic import BaseModel
from typing import List, Optional

class Motivation(BaseModel):
   motivation:str
   auteur:str