from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints
from app.core import database

app = FastAPI(title="GameSphere Analytics API")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    database.init_database()

# CORS configuration
from app.core.config import settings
origins = settings.ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to GameSphere Analytics API"}
