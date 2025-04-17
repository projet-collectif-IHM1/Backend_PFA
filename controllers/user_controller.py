from fastapi import APIRouter, HTTPException
from models.user import User
from config import SECRET_KEY, MONGO_URI, MONGO_DB
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
import jwt
import datetime
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import List, Optional

user_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]
def get_objectid(id: str):
    try:
        return ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@user_router.post("/register/")
async def register(user: User):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    hashed_password = pwd_context.hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password

    result = await db.users.insert_one(user_data)
    return {"id": str(result.inserted_id), "message": "Utilisateur créé avec succès"}

@user_router.post("/login/")
async def signin(user_data: dict):
    existing_user = await db.users.find_one({"email": user_data.get("email")})
    
    if not existing_user or not pwd_context.verify(user_data.get("password"), existing_user["password"]):
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")

    token = jwt.encode(
        {
            "user_id": str(existing_user["_id"]),
            "role": existing_user.get("role", "user"),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return {"token": token, "role": existing_user.get("role", "user"), "message": "Connexion réussie"}
@user_router.get("/", response_model=List[User])
async def get_users():
    users = await db.users.find().to_list(100)

    # Convertir _id en string et l'ajouter en tant que 'id'
    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]  # Supprimer _id original si nécessaire

    return JSONResponse(status_code=200, content={"status_code": 200, "users": users})

@user_router.put("/{user_id}", response_model=dict)
async def update_user(user_id: str, user: User):
    result = await db.users.update_one({"_id": get_objectid(user_id)}, {"$set": user.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

@user_router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    # Supprimer d'abord toutes les réservations associées à cet utilisateur

    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@user_router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    return user