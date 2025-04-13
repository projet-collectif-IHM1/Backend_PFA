from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 🔴 Ajouté pour le CORS
from controllers.user_controller import user_router  
from controllers.categorie_controller import cat_router
from controllers.background_controller import vid_router
from controllers.motivation_controller import mot_router
from controllers.but_controller import but_router

app = FastAPI()

# 🔵 CORS pour autoriser Angular (localhost:4200)
origins = [
    "http://localhost:4200",  # URL de votre application Angular
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔵 Inclusion des routes
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(cat_router, prefix="/categories", tags=["categories"])
app.include_router(vid_router, prefix="/videos", tags=["categories"])
app.include_router(mot_router, prefix="/motivations", tags=["motivations"])
app.include_router(but_router, prefix="/buts", tags=["buts"])

@app.get("/")
async def root():
    return {"message": "FastAPI avec MongoDB 🚀"}
