# app/models.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Odd(BaseModel):
    bookmaker: str
    competition: str        # "Chile Primera División", "Copa Libertadores"
    match_id: str
    home_team: str
    away_team: str
    kickoff: datetime

    market: str             # "1X2", "O/U 2.5"
    selection: str          # "home", "draw", "away", "over", "under"
    odds_decimal: float

    # NUEVO: link de afiliado (puede ser None si no lo tienes aún)
    affiliate_url: Optional[str] = None

    last_updated: datetime
