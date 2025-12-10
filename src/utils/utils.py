import requests
from src.config import settings
TMDB_API_KEY = settings.TMDB_API_KEY



def get_poster_from_title(title_query: str) -> str:
    """
    Recibe un título (ej: "Blade Runner") y devuelve la URL del póster.
    Si algo falla, devuelve una imagen de relleno.
    """
    # 1. URL de la imagen por defecto (Placeholder) para no romper el frontend
    PLACEHOLDER_IMG = "https://via.placeholder.com/500x750?text=No+Poster"
    
    # 2. Validación básica: Si el título viene vacío, cortamos aquí
    if not title_query or not isinstance(title_query, str):
        return PLACEHOLDER_IMG

    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,  # Tu clave '1ecb...'
            "query": title_query,
            "language": "en-US",      # Usamos en-US ya que dijiste que los títulos vienen en inglés
            "page": 1,
            "include_adult": "false"
        }
        
        # 3. Petición con Timeout (seguridad anti-cuelgues)
        # Si TMDB tarda más de 3 segundos, salta al 'except'
        response = requests.get(url, params=params, timeout=3)
        
        # Si la API devuelve error (404, 500), lanzamos excepción
        response.raise_for_status()
        
        data = response.json()
        
        # 4. Verificación de resultados
        # ¿Existe la lista 'results'? ¿Tiene al menos 1 elemento?
        if data.get("results") and len(data["results"]) > 0:
            
            # Cogemos el primer resultado (el más probable)
            first_match = data["results"][0]
            poster_path = first_match.get("poster_path")
            
            # ¿Tiene ruta de póster? (A veces es None)
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
                
    except Exception as e:
        # Aquí puedes poner un print si quieres depurar errores en consola
        # print(f"Error buscando poster para '{title_query}': {e}")
        pass

    # 5. Si llegamos aquí, es que algo falló o no se encontró -> Devolvemos Placeholder
    return PLACEHOLDER_IMG