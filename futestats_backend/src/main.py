from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.team_routes import router as team_router
from src.routes.stadium_routes import router as stadium_router


app = FastAPI(
    title="FuteStats BR API",
    description="Estatísticas e Rankings do Futebol Brasileiro",
    version="0.1.0"
)

app.include_router(team_router)
app.include_router(stadium_router)

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
