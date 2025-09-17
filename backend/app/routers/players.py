from fastapi import APIRouter, HTTPException
from app.services.espn_service import fetch_players_by_team

router = APIRouter()

@router.get("/league/{league_id}/team/{team_id}/players")
def get_team_players(league_id: int, team_id: int):
    """
    Fetches all players for a specific team in a league.
    """
    data = fetch_players_by_team(league_id, team_id)
    if not data:
        raise HTTPException(status_code=404, detail="Team not found")
    return data

