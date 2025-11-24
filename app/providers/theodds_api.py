# app/providers/theodds_api.py
from typing import List, Optional
import re

import httpx

from app.config import (
    settings,
    COMPETITION_TO_SPORT_KEY,
    SPORT_KEY_TO_COMPETITION,
)
from app.models import Odd


def _slug(text: str) -> str:
    """
    Crea un id legible para el partido a partir de los nombres de equipos.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def _build_match_id(bookmaker_key: str, sport_key: str, home_team: str, away_team: str, kickoff: str) -> str:
    """
    Genera un match_id estable combinando casa, deporte y equipos.
    kickoff viene en ISO; usamos solo la fecha (YYYYMMDD) para el id.
    """
    date_part = kickoff[:10].replace("-", "")  # "2025-11-27" -> "20251127"
    return f"{bookmaker_key}-{sport_key}-{_slug(home_team)}-{_slug(away_team)}-{date_part}"


def _competition_from_sport_key(sport_key: str) -> str:
    """
    Convierte un sport_key de The Odds API a nuestro nombre de competición estándar.
    """
    return SPORT_KEY_TO_COMPETITION.get(sport_key, sport_key)


def fetch_odds_from_theodds(
    competition: Optional[str] = None,
    bookmaker: Optional[str] = None,
) -> List[Odd]:
    """
    Llama a The Odds API para la(s) competición(es) requerida(s) y
    transforma la respuesta al modelo Odd.

    - Si competition viene, consultamos solo ese sport_key.
    - Si no viene, consultamos todas las competiciones que tenemos en el mapeo.
    """
    if not settings.THE_ODDS_API_KEY:
        raise RuntimeError("THE_ODDS_API_KEY no está configurado en las variables de entorno")

    # Determinar qué sport_keys consultar
    sport_keys: List[str] = []

    if competition:
        sport_key = COMPETITION_TO_SPORT_KEY.get(competition)
        if not sport_key:
            # Competición desconocida para nuestro mapeo
            return []
        sport_keys.append(sport_key)
    else:
        # Sin filtro de competición: consultamos todas las que conocemos
        sport_keys = list(COMPETITION_TO_SPORT_KEY.values())

    all_odds: List[Odd] = []

    # Cliente HTTP reutilizable
    with httpx.Client(timeout=10.0) as client:
        for sport_key in sport_keys:
            url = f"{settings.THE_ODDS_API_BASE}/{sport_key}/odds"
            params = {
                "apiKey": settings.THE_ODDS_API_KEY,
                # regiones: EU / UK / US / etc., puedes ajustar esto después
                "regions": "eu",
                # mercado head-to-head (1X2)
                "markets": "h2h",
                "oddsFormat": "decimal",
                "dateFormat": "iso",
            }

            resp = client.get(url, params=params)
            resp.raise_for_status()
            events = resp.json()  # lista de partidos

            for ev in events:
                sport_key_resp = ev.get("sport_key", sport_key)
                competition_name = _competition_from_sport_key(sport_key_resp)

                home_team = ev["home_team"]
                away_team = ev["away_team"]
                kickoff = ev["commence_time"]  # ISO string, Pydantic lo parsea

                for bm in ev.get("bookmakers", []):
                    bm_key = bm.get("key")
                    if bookmaker and bm_key != bookmaker:
                        continue

                    last_updated = bm.get("last_update")

                    # Buscar el mercado h2h
                    for market in bm.get("markets", []):
                        if market.get("key") != "h2h":
                            continue

                        outcomes = market.get("outcomes", [])
                        for outcome in outcomes:
                            name = outcome.get("name")
                            price = outcome.get("price")

                            if name == home_team:
                                selection = "home"
                            elif name == away_team:
                                selection = "away"
                            else:
                                # suele ser "Draw" u otro texto
                                selection = "draw"

                            match_id = _build_match_id(
                                bookmaker_key=bm_key,
                                sport_key=sport_key_resp,
                                home_team=home_team,
                                away_team=away_team,
                                kickoff=kickoff,
                            )

                            affiliate_url = f"https://superbet.cl/go/{bm_key}"

                            odd = Odd(
                                bookmaker=bm_key,
                                competition=competition_name,
                                match_id=match_id,
                                home_team=home_team,
                                away_team=away_team,
                                kickoff=kickoff,
                                market="1X2",
                                selection=selection,
                                odds_decimal=price,
                                affiliate_url=affiliate_url,
                                last_updated=last_updated,
                            )
                            all_odds.append(odd)

    return all_odds
