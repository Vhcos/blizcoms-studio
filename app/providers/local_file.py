# app/providers/local_file.py
import json
from pathlib import Path
from typing import List

from app.models import Odd


# Ruta al archivo JSON con las cuotas de prueba
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_odds.json"


def fetch_odds_from_file() -> List[Odd]:
    """
    Lee las cuotas desde un archivo JSON local y las convierte
    al modelo Odd. Esto simula lo que después hará una API real.
    """
    with DATA_PATH.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    # raw es una lista de dicts -> los mapeamos a Odd
    odds: List[Odd] = [Odd(**item) for item in raw]
    return odds
