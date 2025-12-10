import requests
from src.config import settings
TMDB_API_KEY = settings.TMDB_API_KEY


class TMDBClient:
    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.base_url = "https://api.themoviedb.org/3"
        # Imagen de relleno por si todo falla (para que el front no se vea roto)
        self.placeholder = "https://via.placeholder.com/500x750?text=No+Poster"

    
    def get_poster_url(self, titulo_pelicula: str) -> str:
        # 1. Seguridad: Si el título viene vacío, devolvemos placeholder directamente
        if not titulo_pelicula:
            return self.placeholder

        try:
            url = f"{self.base_url}/search/movie"
            params = {
                "api_key": self.api_key,
                "query": titulo_pelicula,
                # Aunque el título venga en Inglés (Rotten Tomatoes), 
                # pedimos resultados en Español para ver si hay póster localizado.
                "language": "es-ES" 
            }
            
            # Timeout de 3 segundos para que tu app no se quede colgada si TMDB va lento
            response = requests.get(url, params=params, timeout=3)
            
            # Si la respuesta no es 200 OK, lanzamos error controlado
            response.raise_for_status()
            
            data = response.json()
            
            # 2. Seguridad: Comprobamos si 'results' existe y no está vacío
            if data.get('results') and len(data['results']) > 0:
                # Cogemos el primero
                mejor_resultado = data['results'][0]
                ruta_poster = mejor_resultado.get('poster_path')
                
                # 3. Seguridad: Comprobamos que poster_path no sea None
                if ruta_poster:
                    return f"https://image.tmdb.org/t/p/w500{ruta_poster}"
            
            # Si llegamos aquí, es que no se encontró nada
            print(f"⚠️ Alerta: No se encontró póster para '{titulo_pelicula}'")
            return self.placeholder

        except requests.exceptions.Timeout:
            print(f"❌ Error: TMDB tardó demasiado en responder para '{titulo_pelicula}'")
            return self.placeholder
        except Exception as e:
            print(f"❌ Error desconocido buscando '{titulo_pelicula}': {e}")
            return self.placeholder
        

tmdb_client = TMDBClient()