from fastapi import FastAPI
from app.routers import league, players

app = FastAPI(title="Fantasy GM Backend")

app.include_router(league.router, prefix="/api", tags=["League"])
app.include_router(players.router, prefix="/api", tags=["Players"])

@app.get("/")
def root():
    return {"message": "Fantasy GM backend is running"}