from fastapi import APIRouter, HTTPException
from models.but import But
from config import SECRET_KEY, MONGO_URI, MONGO_DB
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


but_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

@but_router.post("/")
async def create_hotel(but: But):
    user = await db.users.find_one({"_id": ObjectId(but.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    result = await db.buts.insert_one(but.dict())
    return {"id": str(result.inserted_id)}


@but_router.get("/", response_model=List[But])
async def get_payes():
    cats = await db.buts.find().to_list(100)

    # Convertir _id en string et l'ajouter en tant que 'id'
    for cat in cats:
        cat["id"] = str(cat["_id"])
        del cat["_id"]  # Supprimer _id original si nécessaire

    return JSONResponse(status_code=200, content={"status_code": 200, "buts": cats})

