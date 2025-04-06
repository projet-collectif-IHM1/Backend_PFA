from fastapi import APIRouter, HTTPException
from models.categorie import Categorie
from config import SECRET_KEY, MONGO_URI, MONGO_DB
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from models.background import BackGround


vid_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

@vid_router.post("/")
async def create_video(back:BackGround ):
    # Vérification que l'hôtel existe
    categorie_id = back.categorie_id
    cat = await db.categories.find_one({"_id": ObjectId(categorie_id)})

    if not cat:
        raise HTTPException(status_code=404, detail="categorie not found")

    result = await db.backgrounds.insert_one(back.model_dump())
    
    await db.categories.update_one(
        {"_id": ObjectId(back.categorie_id)},
        {"$push": {"videos": back.model_dump()}}
    )

    return {"id": str(result.inserted_id)}

@vid_router.get("/{video_id}", response_model=BackGround)
async def get_categorie(video_id: str):
    video = await db.backgrounds.find_one({"_id": ObjectId(video_id)})
    if not video:
        raise HTTPException(status_code=404, detail="video non trouvée")

    video["id"] = str(video["_id"])
    del video["_id"]
    return video


@vid_router.get("/", response_model=List[BackGround])
async def get_payes():
    cats = await db.backgrounds.find().to_list(100)

    # Convertir _id en string et l'ajouter en tant que 'id'
    for cat in cats:
        cat["id"] = str(cat["_id"])
        del cat["_id"]  # Supprimer _id original si nécessaire

    return JSONResponse(status_code=200, content={"status_code": 200, "videos": cats})