from fastapi import APIRouter, HTTPException
from models.but import But
from config import SECRET_KEY, MONGO_URI, MONGO_DB
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from fastapi.responses import JSONResponse
from bson import ObjectId

but_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

# Créer un but
@but_router.post("/")
async def create_but(but: But):
    user = await db.users.find_one({"_id": ObjectId(but.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    result = await db.buts.insert_one(but.dict())
    return {"id": str(result.inserted_id)}

# Obtenir tous les buts
@but_router.get("/", response_model=List[But])
async def get_buts():
    buts = await db.buts.find().to_list(100)
    for but in buts:
        but["id"] = str(but["_id"])
        del but["_id"]
    return JSONResponse(status_code=200, content={"status_code": 200, "buts": buts})

# Mettre à jour un but par ID
@but_router.put("/{but_id}", response_model=dict)
async def update_but(but_id: str, but: But):
    result = await db.buts.update_one({"_id": ObjectId(but_id)}, {"$set": but.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="But non trouvé")
    return {"message": "But mis à jour avec succès"}

# Supprimer un but par ID
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

# Obtenir les buts d'un utilisateur par son user_id
@but_router.get("/user/{user_id}", response_model=List[But])
async def get_buts_by_user_id(user_id: str):
    buts = await db.buts.find({"user_id": user_id}).to_list(100)
    if not buts:
        raise HTTPException(status_code=404, detail="Aucun but trouvé pour cet utilisateur")
    for but in buts:
        but["id"] = str(but["_id"])
        del but["_id"]
    return JSONResponse(status_code=200, content={"status_code": 200, "buts": buts})
