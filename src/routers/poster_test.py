# src/routers/poster_test.py
from fastapi import APIRouter
from pydantic import BaseModel
import requests

from src.config import settings
TMDB_API_KEY = settings.TMDB_API_KEY

router = APIRouter()

# El modelo para recibir el título en el JSON
class PosterRequest(BaseModel):
    titulo: str

@router.post("/traer-poster")
def test_poster_endpoint(datos: PosterRequest):
    """
    Recibe un título, llama a TMDB y devuelve solo la URL.
    """
    if not datos.titulo:
        return {"error": "El título está vacío"}

    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": settings.TMDB_API_KEY, # Asegúrate de que se llame así en tu config
            "query": datos.titulo,
            "language": "en-US" # O es-ES, como prefieras
        }
        
        # Hacemos la llamada
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        # Buscamos la imagen
        if data.get("results") and len(data["results"]) > 0:
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                return {"titulo": datos.titulo, "poster_url": full_url}
        
        return {"mensaje": "No se encontró póster", "poster_url": "https://via.placeholder.com/500?text=404"}

    except Exception as e:
        return {"error": str(e)}