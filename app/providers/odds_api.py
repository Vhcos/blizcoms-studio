# app/providers/odds_api.py
from typing import List, Optional

import httpx

from app.config import settings
from app.models import Odd


def fetch_odds_from_api(
    competition: Optional[str] = None,
    bookmaker: Optional[str] = None,
) -> List[Odd]:
    """
    Provider genérico para llamar a una API externa de cuotas.

    Por ahora asume que la API externa devuelve una lista de objetos
    con las mismas claves que Odd. Cuando elijamos un proveedor real,
    aquí haremos el mapeo necesario.
    """
    if not settings.ODDS_API_URL:
        raise RuntimeError("ODDS_API_URL no está configurada en .env")

    params: dict = {}
    if competition:
        params["competition"] = competition
    if bookmaker:
        params["bookmaker"] = bookmaker

    headers: dict = {}
    if settings.ODDS_API_KEY:
        # Esto es genérico; algunos proveedores usan otro header, aquí se cambia.
        headers["Authorization"] = f"Bearer {settings.ODDS_API_KEY}"

    resp = httpx.get(
        settings.ODDS_API_URL,
        params=params,
        headers=headers,
        timeout=10.0,
    )
    resp.raise_for_status()

    data = resp.json()

    # Asumimos que `data` es una lista de dicts compatibles con Odd.
    # Si el proveedor usa otro formato, aquí haces el mapeo.
    odds: List[Odd] = [Odd(**item) for item in data]
    return odds
