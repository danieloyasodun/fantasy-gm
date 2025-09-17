from fastapi import APIRouter, HTTPException
from app.services.espn_service import fetch_players_by_team
from app.helper import get_league

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

@router.get("/league/{league_id}/team/{team_id}/players/detailed")
def get_team_players_detailed(league_id: int, team_id: int, year: int = 2025):
    """
    Fetches all players for a specific team in a league with full stats, projections, and breakdowns.
    """
    league = get_league(league_id, year)

    # Find the team by ID
    team = next((t for t in league.teams if t.team_id == team_id), None)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    detailed_roster = []
    for player in team.roster:
        player_data = {
            "name": player.name,
            "playerId": player.playerId,
            "position": player.position,
            "proTeam": player.proTeam,
            "lineupSlot": getattr(player, "lineupSlot", None),
            "injuryStatus": getattr(player, "injuryStatus", None),
            "acquisitionType": player.acquisitionType,
            "eligibleSlots": player.eligibleSlots,
            "total_points": getattr(player, "total_points", None),
            "avg_points": getattr(player, "avg_points", None),
            "projected_points": getattr(player, "projected_points", None),
            "stats": getattr(player, "stats", None),          # weekly or seasonal stats
            "projected_breakdown": getattr(player, "projected_breakdown", None),
            "schedule": getattr(player, "schedule", None),
        }
        detailed_roster.append(player_data)

    return {
        "team_name": team.team_name,
        "team_id": team.team_id,
        "roster": detailed_roster
    }

