from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import league, players, free_agents

app = FastAPI(title="Fantasy GM Backend")

origins = [
    "http://localhost:3000",   # React dev server
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,      
    allow_methods=["*"],        
    allow_headers=["*"],        
)

app.include_router(league.router, prefix="/api", tags=["League"])
app.include_router(players.router, prefix="/api", tags=["Players"])
app.include_router(free_agents.router, prefix="/api", tags=["Free Agents"])

@app.get("/")
def root():
    return {"message": "Fantasy GM backend is running"}