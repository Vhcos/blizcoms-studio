# app/config.py
from typing import List, Optional
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    """
    Configuración central del motor de cuotas.

    DATA_SOURCE:
      - "local" -> lee desde sample_odds.json
      - "api"   -> llama a un proveedor externo de cuotas
    """

    DATA_SOURCE: str = "local"  # "local" o "api"

    # Cuando uses un proveedor real, los pegas aquí:
    ODDS_API_URL: Optional[str] = None
    ODDS_API_KEY: Optional[str] = None

    # Competencias que nos interesan por defecto
    DEFAULT_COMPETITIONS: List[str] = [
        "Chile Primera División",
        "Copa Libertadores",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
