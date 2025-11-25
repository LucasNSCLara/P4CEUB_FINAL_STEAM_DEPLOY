import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RAWG_API_KEY: str = os.getenv("RAWG_API_KEY", "")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

settings = Settings()
