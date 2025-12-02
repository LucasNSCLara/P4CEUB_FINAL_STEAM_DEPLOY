from typing import List, Optional
from pydantic import BaseModel, EmailStr

class SystemRequirements(BaseModel):
    minimum: Optional[str] = None
    recommended: Optional[str] = None

class ParsedRequirements(BaseModel):
    cpu: Optional[str] = None
    gpu: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    os: Optional[str] = None

class Game(BaseModel):
    id: int
    name: str
    description_raw: Optional[str] = None
    released: Optional[str] = None
    background_image: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[float] = None
    metacritic: Optional[int] = None
    playtime: Optional[int] = None
    platforms: Optional[List[dict]] = None
    genres: Optional[List[dict]] = None
    developers: Optional[List[dict]] = None
    publishers: Optional[List[dict]] = None
    
    # Custom fields for our dashboard
    parsed_requirements_min: Optional[ParsedRequirements] = None
    parsed_requirements_rec: Optional[ParsedRequirements] = None
    file_size: Optional[str] = None
    similar_games: Optional[List[dict]] = None

# Authentication schemas
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    token: str

# Favorites schemas
class FavoriteGame(BaseModel):
    game_id: int
    game_name: str
    game_image: Optional[str] = None
    game_rating: Optional[float] = None

class FavoriteResponse(BaseModel):
    game_id: int
    game_name: str
    game_image: Optional[str] = None
    game_rating: Optional[float] = None
    created_at: str

# Comparison schemas
class CompareRequest(BaseModel):
    game_id: int
    user_cpu: str
    user_gpu: str
    user_ram: str

class CompareResponse(BaseModel):
    can_run_minimum: bool
    can_run_recommended: bool
    details: dict

