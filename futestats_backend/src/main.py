from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="FuteStats BR API",
    description="Estatísticas e Rankings do Futebol Brasileiro",
    version="0.1.0"
)


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

# Exemplo de como as rotas serão organizadas futuramente
# from src.routes import teams, championships
# app.include_router(teams.router, prefix="/v1")