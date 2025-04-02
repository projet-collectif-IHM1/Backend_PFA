from fastapi import APIRouter, HTTPException
from models.categorie import Categorie
from config import SECRET_KEY, MONGO_URI, MONGO_DB
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


cat_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

@cat_router.post("/")
async def create_paye(paye: Categorie):
    result = await db.categories.insert_one(paye.dict())
    return {"id": str(result.inserted_id)} 

@cat_router.get("/", response_model=List[Categorie])
async def get_payes():
    cats = await db.categories.find().to_list(100)

    # Convertir _id en string et l'ajouter en tant que 'id'
    for cat in cats:
        cat["id"] = str(cat["_id"])
        del cat["_id"]  # Supprimer _id original si nécessaire

    return JSONResponse(status_code=200, content={"status_code": 200, "payes": cats})

@cat_router.get("/{categorie_id}", response_model=Categorie)
async def get_categorie(categorie_id: str):
    categorie = await db.categories.find_one({"_id": ObjectId(categorie_id)})
    if not categorie:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")

    categorie["id"] = str(categorie["_id"])
    del categorie["_id"]
    return categorie