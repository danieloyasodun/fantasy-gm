from espn_api.football import League
from app.config import ESPNS2, SWID
from app.helper import get_league

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
    Returns free agents for a league optionally filtered by position and limited by size.
    Includes projected points, stats, and additional player metadata.
    """
    league = get_league(league_id, year)

    # Fetch free agents
    if position:
        agents = league.free_agents(size=size, position=position)
    else:
        agents = league.free_agents(size=size)

    free_agents_data = []
    for player in agents:
        # Extract stats safely
        stats = getattr(player, "stats", {}) or {}

        # Most recent / season-level stats (espn-python uses 0 for season totals, 3 for current week projections)
        season_stats = stats.get(0, {})
        week_projection = stats.get(3, {})

        player_info = {
            "player_id": player.playerId,
            "name": player.name,
            "position": player.position,
            "pos_rank": player.posRank,
            "pro_team": player.proTeam,
            "eligible_slots": player.eligibleSlots,
            "acquisition_type": player.acquisitionType,
            "injury_status": getattr(player, "injuryStatus", None),
            "active_status": getattr(player, "active_status", None),
            "percent_owned": getattr(player, "percent_owned", None),
            "percent_started": getattr(player, "percent_started", None),
            "total_points": season_stats.get("points", 0),
            "avg_points": season_stats.get("avg_points", 0),
            "projected_total_points": season_stats.get("projected_points", 0),
            "projected_avg_points": season_stats.get("projected_avg_points", 0),
            "stats": {
                "season": {
                    "points": season_stats.get("points", 0),
                    "breakdown": season_stats.get("breakdown", {}),
                    "projected_points": season_stats.get("projected_points", 0),
                    "projected_breakdown": season_stats.get("projected_breakdown", {}),
                },
                "week_projection": {
                    "projected_points": week_projection.get("projected_points", 0),
                    "projected_breakdown": week_projection.get("projected_breakdown", {}),
                },
            },
            "opponent": getattr(player, "pro_opponent", None),
            "game_date": getattr(player, "game_date", None),
            "on_bye_week": getattr(player, "on_bye_week", False),
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
    Returns league settings like number of teams, season length, veto votes,
    scoring categories (ids, names, points), and position slot counts.
    """
    league = get_league(league_id, year)
    settings = league.settings

    # Build a cleaner scoring categories list
    scoring_categories = [
        {
            "id": cat["id"],
            "abbr": cat["abbr"],
            "label": cat["label"],
            "points": cat["points"],
        }
        for cat in getattr(settings, "scoring_format", [])
    ]

    return {
        "league_name": settings.name,
        "team_count": settings.team_count,
        "regular_season_count": settings.reg_season_count,
        "veto_votes_required": settings.veto_votes_required,
        "playoff_team_count": settings.playoff_team_count,
        "keeper_count": settings.keeper_count,
        "scoring_type": settings.scoring_type,
        "faab_enabled": settings.faab,
        "acquisition_budget": settings.acquisition_budget,
        "position_slot_counts": getattr(settings, "position_slot_counts", {}),
        "scoring_categories": scoring_categories,
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

def fetch_scoreboard(league_id: int, week: int, year: int = 2025):
    """
    Returns matchups for a given week with socres
    """
    league = get_league(league_id, year)
    matchups = league.scoreboard(week)

    data = []
    for matchup in matchups:
        data.append({
            "home_team": matchup.home_team.team_name,
            "home_team_id": matchup.home_team.team_id,
            "home_score": matchup.home_score,
            "away_team": matchup.away_team.team_name,
            "away_team_id": matchup.away_team.team_id,
            "away_score": matchup.away_score
        })
    return data


def fetch_box_scores(league_id: int, week: int, year: int = 2025):
    """
    Returns detailed box scores for a given week, including player stats.
    """
    league = get_league(league_id, year)
    box_scores = league.box_scores(week)
    
    data = []
    for matchup in box_scores:
        def serialize_lineup(lineup):
            return [
                {
                    "name": player.name,
                    "position": player.position,
                    "slot_position": player.slot_position,
                    "points": player.points,
                    "projected_points": player.projected_points,
                    "pro_opponent": player.pro_opponent,
                    "pro_pos_rank": player.pro_pos_rank
                }
                for player in lineup
            ]
        
        data.append({
            "home_team": matchup.home_team.team_name,
            "home_team_id": matchup.home_team.team_id,
            "home_score": matchup.home_score,
            "home_lineup": serialize_lineup(matchup.home_lineup),
            "away_team": matchup.away_team.team_name,
            "away_team_id": matchup.away_team.team_id,
            "away_score": matchup.away_score,
            "away_lineup": serialize_lineup(matchup.away_lineup)
        })
    
    return data

def fetch_recent_activity(league_id: int, size: int = 25, msg_type: str = None, year: int = 2025):
    """
    Returns recent activity for a league, optionally filtered by message type.
    """
    league = get_league(league_id, year)
    
    activity_list = league.recent_activity(msg_type=msg_type) if msg_type else league.recent_activity()
    activity_list = activity_list[:size]

    serialized_activity = []

    for activity in activity_list:
        actions_data = []

        for action in activity.actions:
            if len(action) == 3:
                team, act_type, player_name = action
                actions_data.append({
                    "team_name": team.team_name,
                    "team_id": team.team_id,
                    "action": act_type,
                    "player_name": player_name
                })
            elif len(action) == 5:
                # TRADED: (team1, 'TRADED', player1, team2, player2)
                team1, act_type, player1, team2, player2 = action
                actions_data.append({
                    "team_name": team1.team_name,
                    "team_id": team1.team_id,
                    "action": act_type,
                    "player_name": player1
                })
                actions_data.append({
                    "team_name": team2.team_name,
                    "team_id": team2.team_id,
                    "action": act_type,
                    "player_name": player2
                })
            else:
                # fallback for unexpected structure
                actions_data.append({"raw_action": str(action)})

        serialized_activity.append({
            "timestamp": getattr(activity, "timestamp", None),
            "type": getattr(activity, "type", None),
            "actions": actions_data
        })

    return serialized_activity

def fetch_top_scorer(league_id: int, year: int = 2025):
    """
    Returns the team with the highest total points in the league.
    """
    league = get_league(league_id, year)

    # Find the team with the maximum points
    top_team = max(league.teams, key=lambda t: t.points_for)
    
    return {
        "team_name": top_team.team_name,
        "points": top_team.points_for
    }

def fetch_lowest_scorer(league_id: int, year: int = 2025):
    """
    Returns the team with the lowest total points in the league.
    """
    league = get_league(league_id, year)
    
    lowest_team = min(league.teams, key=lambda t: t.points_for)
    
    return {
        "team_name": lowest_team.team_name,
        "points": lowest_team.points_for,
        "wins": lowest_team.wins,
        "losses": lowest_team.losses
    }

def fetch_league_point_order(league_id: int, year: int = 2025):
    """
    Returns all teams in the league, sorted from most to least points.
    """
    league = League(
        league_id=league_id,
        year=year,
        espn_s2=ESPNS2,
        swid=SWID,
        debug=False
    )
    
    # Sort teams by points_for descending
    sorted_teams = sorted(league.teams, key=lambda t: t.points_for, reverse=True)
    
    return [
        {"team_name": team.team_name, "points": team.points_for, "wins": team.wins, "losses": team.losses}
        for team in sorted_teams
    ]