from fastapi import FastAPI
from app.routers import league, players, free_agents

app = FastAPI(title="Fantasy GM Backend")

app.include_router(league.router, prefix="/api", tags=["League"])
app.include_router(players.router, prefix="/api", tags=["Players"])
app.include_router(free_agents.router, prefix="/api", tags=["Free Agents"])

@app.get("/")
def root():
    return {"message": "Fantasy GM backend is running"}