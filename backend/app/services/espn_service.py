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

def fetch_league_teams_detailed(league_id: int, year: int = 2025):
    """
    Fetches teams with basic info and roster
    """
    league = get_league(league_id, year)

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
    league = get_league(league_id, year)

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

def fetch_free_agents(league_id: int, size: int = 20, position: str = None, year: int = 2025):
    """
    Returns free agents for a league optionally filtered by position and limited by size
    """
    league = get_league(league_id, year)

    # Fetch free agents
    if position:
        agents = league.free_agents(size=size, position=position)
    else:
        agents = league.free_agents(size=size)

    # Convert to JSON-serializable dicts
    free_agents_data = []
    for player in agents:
        player_info = {
            "player_id": player.playerId,
            "name": player.name,
            "position": player.position,
            "pos_rank": player.posRank,
            "pro_team": player.proTeam,
            "eligible_slots": player.eligibleSlots,
            "acquisition_type": player.acquisitionType
        }
        free_agents_data.append(player_info)

    return free_agents_data

def fetch_draft(league_id: int, year: int = 2025):
    """
    Returns draft picks for the league.
    """
    league = get_league(league_id, year)

    draft_data = []
    for pick in league.draft:
        draft_data.append({
            "player_name": pick.playerName,
            "round": pick.round_num,
            "round_pick": pick.round_pick,
            "team_name": pick.team.team_name,
            "team_id": pick.team.team_id
        })
    
    return draft_data

def fetch_league_settings(league_id: int, year: int = 2025):
    """
    Returns league settings like number of teams, season length, and veto votes.
    """
    league = get_league(league_id, year)
    settings = league.settings

    return {
        "team_count": settings.team_count,
        "regular_season_count": settings.reg_season_count,
        "veto_votes_required": settings.veto_votes_required
    }

def fetch_power_rankings(league_id: int, week: int, year: int = 2025):
    """
    Returns power rankings for a league for a given week.
    """
    league = get_league(league_id, year)
    rankings = league.power_rankings(week=week)

    rankings_data = []
    for score, team in rankings:
        rankings_data.append({
            "team_name": team.team_name,
            "team_id": team.team_id,
            "score": float(score)
        })
    
    return rankings_data