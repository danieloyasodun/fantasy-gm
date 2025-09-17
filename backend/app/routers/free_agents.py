from fastapi import APIRouter, Query
from app.services.espn_service import fetch_free_agents

router = APIRouter()

@router.get("/league/{league_id}/free-agents")
def get_free_agents(
    league_id: int,
    size: int = Query(20, description="Number of free agents to return"),
    position: str = Query(None, description="Filter by position, e.g., QB, WR, RB, TE")
):
    """
    Fetches free agents in a league, optionally filtered by position.
    """
    data = fetch_free_agents(league_id, size=size, position=position)
    return data
