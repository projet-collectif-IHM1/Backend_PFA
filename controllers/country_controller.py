from fastapi import APIRouter, HTTPException
from models.country import Country
from config import SECRET_KEY, MONGO_URI, MONGO_DB
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


pays_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

@pays_router.post("/")
async def create_pays(pays: Country):
    result = await db.countries.insert_one(pays.dict())
    return {"id": str(result.inserted_id)} 

@pays_router.get("/", response_model=List[Country])
async def get_pays():
    cats = await db.countries.find().to_list(400)

    # Convertir _id en string et l'ajouter en tant que 'id'
    for cat in cats:
        cat["id"] = str(cat["_id"])
        del cat["_id"]  # Supprimer _id original si nécessaire

    return JSONResponse(status_code=200, content={"status_code": 200, "payes": cats})

@pays_router.get("/{pays_id}", response_model=Country)
async def get_pays(pays_id: str):
    pays = await db.countries.find_one({"_id": ObjectId(pays_id)})
    if not pays:
        raise HTTPException(status_code=404, detail="pays non trouvée")

    pays["id"] = str(pays["_id"])
    del pays["_id"]
    return pays
