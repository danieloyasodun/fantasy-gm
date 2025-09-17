from fastapi import APIRouter
from app.services.espn_service import fetch_league_teams_detailed

router = APIRouter()

@router.get("/league/{league_id}")
def get_league(league_id: int):
    """
    Fetches all teams in the league with basic info and roster
    """
    data = fetch_league_teams_detailed(league_id)
    return data
