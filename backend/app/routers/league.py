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

def fetch_team_by_id(league_id: int, team_id: int):
    teams = fetch_league_teams_detailed(league_id)
    for team in teams:
        if team['team_id'] == team_id: 
            return team
    return None 

@router.get("/league/{league_id}")
def get_league_info(league_id: int):
    """
    Fetches all teams in the league with basic info and roster
    """
    data = fetch_league_teams_detailed(league_id)
    if not data:
        raise HTTPException(status_code=404, detail="League data not found")
    return data

@router.get("/league/{league_id}/team/{team_id}")
def get_team(league_id: int, team_id: int):
    """
    Fetches specific team in the league with basic info and roster
    """
    team = fetch_team_by_id(league_id, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team 

@router.get("/league/{league_id}/team/{team_id}/detailed")
def get_team_detailed(league_id: int, team_id: int, year: int = 2025):
    """
    Fetches a specific team in a league with full stats, projections, and breakdowns.
    """
    league = get_league(league_id, year)

    # Find the team by ID
    team = next((t for t in league.teams if t.team_id == team_id), None)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    detailed_team = {
        "team_id": team.team_id,
        "team_abbrev": getattr(team, "team_abbrev", None),
        "team_name": team.team_name,
        "division_id": getattr(team, "division_id", None),
        "division_name": getattr(team, "division_name", None),
        "wins": team.wins,
        "losses": team.losses,
        "ties": getattr(team, "ties", 0),
        "points_for": getattr(team, "points_for", 0.0),
        "points_against": getattr(team, "points_against", 0.0),
        "acquisitions": getattr(team, "acquisitions", 0),
        "acquisition_budget_spent": getattr(team, "acquisition_budget_spent", 0),
        "drops": getattr(team, "drops", 0),
        "trades": getattr(team, "trades", 0),
        "move_to_ir": getattr(team, "move_to_ir", 0),
        "playoff_pct": getattr(team, "playoff_pct", 0.0),
        "draft_projected_rank": getattr(team, "draft_projected_rank", None),
        "streak_length": getattr(team, "streak_length", 0),
        "streak_type": getattr(team, "streak_type", None),
        "standing": getattr(team, "standing", None),
        "final_standing": getattr(team, "final_standing", None),
        "waiver_rank": getattr(team, "waiver_rank", None),
        "logo_url": getattr(team, "logo_url", None),
        # Convert schedule to dicts with only basic info
        "schedule": [{"team_id": t.team_id, "team_name": t.team_name} for t in getattr(team, "schedule", [])],
        # Convert roster to dicts with only basic info
        "roster": [{"name": p.name, "playerId": p.playerId, "position": p.position} for p in getattr(team, "roster", [])],
        "scores": getattr(team, "scores", []),
        "outcomes": getattr(team, "outcomes", []),
        "mov": getattr(team, "mov", []),
        "stats": getattr(team, "stats", {}),
    }


    return detailed_team

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