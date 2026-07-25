from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import os

from src.routes.team_routes import router as team_router
from src.routes.stadium_routes import router as stadium_router
from src.routes.competition_routes import router as competition_router
from src.routes.edition_routes import router as edition_router
from src.routes.phase_routes import router as phase_router
from src.routes.round_routes import router as round_router



app = FastAPI(
    title="FuteStats BR API",
    description="Estatísticas e Rankings do Futebol Brasileiro",
    version="0.1.0"
)


os.makedirs("src/static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="src/static"), name="static") 

app.include_router(team_router)
app.include_router(stadium_router)
app.include_router(competition_router)
app.include_router(edition_router)
app.include_router(phase_router)
app.include_router(round_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "message": "FuteStats BR API está online!",
        "docs": "/docs",
        "version": "0.1.0"
    }
