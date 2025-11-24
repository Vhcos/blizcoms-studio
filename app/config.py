# app/config.py
from typing import List, Optional
from pydantic_settings import BaseSettings

# Mapeo entre el nombre "bonito" que usamos nosotros
# y el sport_key de The Odds API
COMPETITION_TO_SPORT_KEY = {
    "Chile Primera División": "soccer_chile_campeonato",
    "Copa Libertadores": "soccer_conmebol_copa_libertadores",
    "Copa Sudamericana":"soccer_conmebol_copa_sudamericana",
}

# Inverso: desde sport_key a nuestro nombre estándar
SPORT_KEY_TO_COMPETITION = {
    v: k for k, v in COMPETITION_TO_SPORT_KEY.items()
}


class Settings(BaseSettings):
    """
    Configuración central del motor de cuotas.

    DATA_SOURCE:
      - "local"   -> lee desde sample_odds.json
      - "theodds" -> usa The Odds API como origen
    """

    DATA_SOURCE: str = "local"

    # The Odds API
    THE_ODDS_API_KEY: Optional[str] = None
    THE_ODDS_API_BASE: str = "https://api.the-odds-api.com/v4/sports"
    
    # Whitelist de casas que queremos mostrar en SuperBet
    ALLOWED_BOOKMAKERS: List[str] = [
        "betsson",
        "coolbet",
        "jugabet",
        "estelarbet",
        "1win",
    ]

    # Competencias que nos interesan por defecto
    DEFAULT_COMPETITIONS: List[str] = list(COMPETITION_TO_SPORT_KEY.keys())
    
    

    class Config:
        env_file = ".env"


settings = Settings()
