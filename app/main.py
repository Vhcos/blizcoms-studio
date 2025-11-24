# app/main.py
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import Odd
from .services import get_odds

app = FastAPI(title="Blizcoms Odds Engine", version="0.1.0")

# CORS: por ahora dejamos abierto para no pelear con el front.
# Después se puede restringir a ["https://superbet.cl", "https://www.superbet.cl"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Blizcoms Odds Engine está arriba. Prueba /health, /odds o /docs."
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "blizcoms-studio"}


@app.get("/odds", response_model=List[Odd])
def get_odds_endpoint(
    competition: Optional[str] = None,
    bookmaker: Optional[str] = None,
):
    return get_odds(competition=competition, bookmaker=bookmaker)
