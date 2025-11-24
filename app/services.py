# app/services.py
from typing import List, Optional

from .config import settings
from .models import Odd
from .providers.local_file import fetch_odds_from_file
from .providers.theodds_api import fetch_odds_from_theodds


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

      - DATA_SOURCE = "local"   -> lee JSON local (sample_odds.json)
      - DATA_SOURCE = "theodds" -> usa The Odds API como origen

    Siempre aplica los filtros al final.
    """
    if settings.DATA_SOURCE == "theodds":
        odds = fetch_odds_from_theodds(
            competition=competition,
            bookmaker=bookmaker,
        )
    else:
        # Modo desarrollo / offline: archivo local
        odds = fetch_odds_from_file()

    odds = _apply_filters(odds, competition, bookmaker)
    return odds
