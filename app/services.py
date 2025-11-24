# app/services.py
from typing import List, Optional

from .config import settings
from .models import Odd
from .providers.local_file import fetch_odds_from_file
from .providers.odds_api import fetch_odds_from_api


def _apply_filters(
    odds: List[Odd],
    competition: Optional[str],
    bookmaker: Optional[str],
) -> List[Odd]:
    if competition:
        odds = [o for o in odds if o.competition == competition]

    if bookmaker:
        odds = [o for o in odds if o.bookmaker == bookmaker]

    return odds


def get_odds(
    competition: Optional[str] = None,
    bookmaker: Optional[str] = None,
) -> List[Odd]:
    """
    Orquesta la obtención de cuotas:
      - Si DATA_SOURCE = "local" -> lee JSON local.
      - Si DATA_SOURCE = "api"   -> llama a un proveedor externo.

    Siempre aplica los filtros al final.
    """
    if settings.DATA_SOURCE == "api":
        odds = fetch_odds_from_api(competition=competition, bookmaker=bookmaker)
        # Si la API ya filtra por competition/bookmaker, esto igual es seguro.
    else:
        # Modo desarrollo / offline: archivo local
        odds = fetch_odds_from_file()

    odds = _apply_filters(odds, competition, bookmaker)
    return odds
