from espn_api.football import League
from app.config import ESPNS2, SWID

def get_league(league_id: int, year: int = 2025, debug: bool = False) -> League:
    """
    Initializes and returns an ESPN League object.
    """
    return League(
        league_id=league_id,
        year=year,
        espn_s2=ESPNS2,
        swid=SWID,
        debug=debug
    )