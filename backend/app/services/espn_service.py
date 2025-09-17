from espn_api.football import League
from app.config import ESPNS2, SWID

def fetch_league_teams_detailed(league_id: int, year: int = 2025):
    """
    Fetches teams with basic info and roster
    """
    league = League(
        league_id=league_id,
        year=year,
        espn_s2=ESPNS2,
        swid=SWID,
        debug=False
    )

    teams_data = []
    for team in league.teams:
        team_info = {
            "team_name": team.team_name,
            "team_id": team.team_id,
            "wins": team.wins,
            "losses": team.losses,
            "final_standing": team.final_standing,
            "roster": [player.name for player in team.roster],  # just names
        }
        teams_data.append(team_info)

    return teams_data

def fetch_players_by_team(league_id: int, team_id: int, year: int = 2025):
    """
    Returns detailed player info for a specific team in a league.
    """
    league = League(
        league_id=league_id,
        year=year,
        espn_s2=ESPNS2,
        swid=SWID,
        debug=False
    )

    # Find the team by ID
    team = next((t for t in league.teams if t.team_id == team_id), None)
    if not team:
        return []  # or raise HTTPException in router

    players_data = []
    for player in team.roster:
        player_info = {
            "player_id": player.playerId,
            "name": player.name,
            "position": player.position,
            "pos_rank": player.posRank,
            "pro_team": player.proTeam,
            "eligible_slots": player.eligibleSlots,
            "acquisition_type": player.acquisitionType,
            "team_id": team.team_id,
            "team_name": team.team_name
        }
        players_data.append(player_info)

    return players_data