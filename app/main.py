# app/main.py
from typing import List, Optional

from fastapi import FastAPI

from .models import Odd
from .services import get_odds

app = FastAPI(title="Blizcoms Odds Engine")


@app.get("/")
def root():
    return {"message": "Blizcoms Odds Engine está arriba. Prueba /health, /odds o /docs."}


@app.get("/health")
def health():
    return {"status": "ok", "service": "blizcoms-studio"}


@app.get("/odds", response_model=List[Odd])
def get_odds_endpoint(
    competition: Optional[str] = None,
    bookmaker: Optional[str] = None,
):
    """
    Devuelve las cuotas normalizadas.
    Filtros opcionales:
    - competition: nombre exacto de la competición
    - bookmaker: nombre exacto de la casa (betsson, coolbet, etc.)
    """
    return get_odds(competition=competition, bookmaker=bookmaker)
