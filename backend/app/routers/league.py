from fastapi import APIRouter, HTTPException, Query
from app.services.espn_service import (
    fetch_league_teams_detailed, 
    fetch_draft, 
    fetch_league_settings, 
    fetch_power_rankings
)

router = APIRouter()

@router.get("/league/{league_id}")
def get_league(league_id: int):
    """
    Fetches all teams in the league with basic info and roster
    """
    data = fetch_league_teams_detailed(league_id)
    if not data:
        raise HTTPException(status_code=404, detail="League data not found")
    return data

@router.get("/league/{league_id}/draft")
def get_draft(league_id: int):
    """
    Returns all draft picks for a league.
    """
    data = fetch_draft(league_id)
    if not data:
        raise HTTPException(status_code=404, detail="Draft data not found")
    return data


@router.get("/league/{league_id}/settings")
def get_settings(league_id: int):
    """
    Returns league settings such as team count, season length, and veto votes.
    """
    data = fetch_league_settings(league_id)
    if not data:
        raise HTTPException(status_code=404, detail="League settings not found")
    return data

@router.get("/league/{league_id}/power-rankings")
def get_power_rankings(league_id: int, week: int = Query(..., description="Week number")):
    """
    Returns power rankings for a given league and week
    """
    data = fetch_power_rankings(league_id, week)
    if not data:
        raise HTTPException(status_code=404, detail="Power rankings not found")
    return data
