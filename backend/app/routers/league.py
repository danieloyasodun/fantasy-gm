from fastapi import APIRouter, HTTPException, Query
from ff_espn_api import League 
from app.helper import get_league
from app.services.espn_service import (
    fetch_league_teams_detailed, 
    fetch_draft, 
    fetch_league_settings, 
    fetch_power_rankings,
    fetch_box_scores,
    fetch_scoreboard,
    fetch_recent_activity,
    fetch_top_scorer,
    fetch_lowest_scorer,
    fetch_league_point_order,
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

@router.get("/league/{league_id}/scoreboard")
def get_scoreboard(league_id: int, week: int = Query(..., description="Week number")):
    """
    Returns the scoreboard for a league for a specific week.
    """
    data = fetch_scoreboard(league_id, week)
    if not data:
        raise HTTPException(status_code=404, detail="Scoreboard not found")
    return data


@router.get("/league/{league_id}/box-scores")
def get_box_scores(league_id: int, week: int = Query(..., description="Week number")):
    """
    Returns detailed box scores for a league for a specific week, including player stats.
    """
    data = fetch_box_scores(league_id, week)
    if not data:
        raise HTTPException(status_code=404, detail="Box scores not found")
    return data

@router.get("/league/{league_id}/activity")
def get_recent_activity(
    league_id: int,
    size: int = Query(25, description="Number of activity items to return"),
    msg_type: str = Query(None, description="Filter by message type, e.g., 'TRADED'")
):
    """
    Returns recent activity for a league, optionally filtered by type (TRADED, DROPPED, ADDED, etc.).
    """
    data = fetch_recent_activity(league_id, size=size, msg_type=msg_type)
    if not data:
        raise HTTPException(status_code=404, detail="No recent activity found")
    return data

@router.get("/league/{league_id}/top_scorer")
def get_top_scorer(league_id: int, year: int = 2025):
    """
    Returns the team with the most points in the league.
    """
    return fetch_top_scorer(league_id, year)

@router.get("/league/{league_id}/lowest_scorer")
def get_lowest_scorer(league_id: int, year: int = 2025):
    """
    Returns the team with the lowest total points in the league.
    """
    return fetch_lowest_scorer(league_id, year)

@router.get("/league/{league_id}/point_order")
def get_league_point_order(league_id: int, year: int = 2025):
    """
    Returns all teams in the league sorted from highest to lowest points
    """
    return fetch_league_point_order(league_id, year)