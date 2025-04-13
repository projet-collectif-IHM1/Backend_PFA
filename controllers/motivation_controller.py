from fastapi import APIRouter, HTTPException
from models.motivation import Motivation
from config import SECRET_KEY, MONGO_URI, MONGO_DB
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


mot_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

@mot_router.post("/")
async def create_paye(paye: Motivation):
    result = await db.motivation.insert_one(paye.dict())
    return {"id": str(result.inserted_id)} 

@mot_router.get("/", response_model=List[Motivation])
async def get_payes():
    cats = await db.motivation.find().to_list(100)

    # Convertir _id en string et l'ajouter en tant que 'id'
    for cat in cats:
        cat["id"] = str(cat["_id"])
        del cat["_id"]  # Supprimer _id original si nécessaire

    return JSONResponse(status_code=200, content={"status_code": 200, "motivations": cats})


