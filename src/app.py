# src/app.py
from fastapi import FastAPI
from src.config import settings
from src.routers.recommend import router as recommend_router
from src.routers.poster_test import router as poster_router

app = FastAPI(title="Movie RA API", version="0.1.0")
app.include_router(recommend_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok", "chroma": settings.CHROMA_PATH}

app.include_router(poster_router, prefix="/api")