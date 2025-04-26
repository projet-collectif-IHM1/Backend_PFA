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

@but_router.get("/{but_id}", response_model=But)
async def get_but_by_id(but_id: str):
    but = await db.buts.find_one({"_id": ObjectId(but_id)})
    if not but:
        raise HTTPException(status_code=404, detail="But non trouvé")
    return but  # Retourne l'objet but directement

@but_router.put("/{but_id}", response_model=dict)
async def update_but(but_id: str, but: But):
    result = await db.buts.update_one({"_id": ObjectId(but_id)}, {"$set": but.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="But not found")
    return {"message": "But updated successfully"}


@but_router.delete("/{but_id}", response_model=dict)
async def delete_but(but_id: str):
    try:
        oid = ObjectId(but_id)
    except:
        raise HTTPException(status_code=400, detail="ID invalide")

    result = await db.buts.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="But non trouvé")

    return JSONResponse(status_code=200, content={"status_code": 200, "message": "But supprimé avec succès"})


