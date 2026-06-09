from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import kiselka, games

app = FastAPI(
    title="Kiselka API",
    description="API для управления Киселькой",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(kiselka.router)
app.include_router(games.router)

@app.get("/")
async def root():
    return {
        "message": "Kiselka API is running! 🎮",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}