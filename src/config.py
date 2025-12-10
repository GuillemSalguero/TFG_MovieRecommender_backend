# src/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict  # 👈 OJO: viene de pydantic_settings, NO de pydantic

class Settings(BaseSettings):
    CHROMA_PATH: str = "C:/Users/guill/Desktop/dataSets/data/vector_db"
    SUPABASE_URL: str
    SUPABASE_KEY: str
    TOP_K: int = 5
    TMDB_API_KEY: str = "1ecb334da1e4a8ee1e5b730459c80e95"

    # Puedes añadir otras configuraciones globales aquí
    IDIOMA_RESPUESTA: str = "es-ES"
    # Configuración para Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()

