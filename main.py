from fastapi import FastAPI
from controllers.user_controller import user_router  
from controllers.categorie_controller import cat_router

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(cat_router, prefix="/categories", tags=["categories"])
@app.get("/")
async def root():
    return {"message": "FastAPI avec MongoDB 🚀"}