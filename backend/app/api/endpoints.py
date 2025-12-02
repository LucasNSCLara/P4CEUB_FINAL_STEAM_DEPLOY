from fastapi import APIRouter, HTTPException, Query, Depends
import requests
from app.core.config import settings
from app.models.schemas import (
    Game, ParsedRequirements, UserRegister, UserLogin, UserResponse,
    FavoriteGame, FavoriteResponse, CompareRequest, CompareResponse
)
from app.core.parser import parse_requirements
from app.services.rawg_service import rawg_service
from app.core import database, auth, comparator
import json
import redis

router = APIRouter()

# Initialize Redis
try:
    r = redis.from_url(settings.REDIS_URL, decode_responses=True)
except Exception as e:
    print(f"Warning: Redis connection failed: {e}")
    r = None

RAWG_BASE_URL = "https://api.rawg.io/api"

@router.get("/search")
async def search_games(query: str = Query(..., min_length=1)):
    """
    Search for games with autocomplete suggestions.
    """
    if not query:
        return {"results": []}
    
    data = await rawg_service.search_games(query, page_size=5)
    
    # Simplify the response for autocomplete
    suggestions = []
    for game in data.get("results", []):
        suggestions.append({
            "id": game.get("id"),
            "name": game.get("name"),
            "slug": game.get("slug"),
            "background_image": game.get("background_image"),
            "rating": game.get("rating"),
            "released": game.get("released")
        })
    
    return {"results": suggestions}

@router.get("/game/{game_name}", response_model=Game)
async def get_game_details(game_name: str):
    """
    Fetch game details from RAWG, parse system requirements, and return aggregated data.
    """
    if not settings.RAWG_API_KEY:
        raise HTTPException(status_code=500, detail="RAWG API Key not configured")

    # Check cache
    cache_key = f"game:{game_name}"
    if r:
        try:
            cached_data = r.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis cache read failed: {e}")

    # Fetch from RAWG
    # First search for the game to get the ID/slug
    search_url = f"{RAWG_BASE_URL}/games"
    params = {
        "key": settings.RAWG_API_KEY,
        "search": game_name,
        "page_size": 1
    }
    
    try:
        print(f"Searching for game: {game_name}")
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"Search response received, results count: {len(data.get('results', []))}")
        
        if not data.get("results"):
            raise HTTPException(status_code=404, detail="Game not found")
            
        game_slug = data["results"][0]["slug"]
        print(f"Found game slug: {game_slug}")
        
        # Get detailed info
        detail_url = f"{RAWG_BASE_URL}/games/{game_slug}"
        print(f"Fetching game details from: {detail_url}")
        detail_response = requests.get(detail_url, params={"key": settings.RAWG_API_KEY, "language": "por"}, timeout=10)
        detail_response.raise_for_status()
        game_data = detail_response.json()
        print(f"Game details received for: {game_data.get('name')}")
        
        # Parse requirements
        platforms = game_data.get("platforms", [])
        pc_requirements = {}
        
        for p in platforms:
            if p.get("platform", {}).get("slug") == "pc":
                pc_requirements = p.get("requirements", {})
                break
        
        print(f"PC requirements found: {bool(pc_requirements)}")
        parsed_min = parse_requirements(pc_requirements.get("minimum", ""))
        parsed_rec = parse_requirements(pc_requirements.get("recommended", ""))
        
        # Construct response
        game_obj = Game(
            id=game_data["id"],
            name=game_data["name"],
            description_raw=game_data.get("description_raw"),
            released=game_data.get("released"),
            background_image=game_data.get("background_image"),
            website=game_data.get("website"),
            rating=game_data.get("rating"),
            metacritic=game_data.get("metacritic"),
            playtime=game_data.get("playtime"),
            platforms=game_data.get("platforms"),
            genres=game_data.get("genres"),
            developers=game_data.get("developers"),
            publishers=game_data.get("publishers"),
            parsed_requirements_min=parsed_min,
            parsed_requirements_rec=parsed_rec,
            file_size=parsed_min.storage if parsed_min.storage else parsed_rec.storage,
            similar_games=[]
        )

        # Fetch similar games
        game_obj.similar_games = []  # Initialize empty list
        try:
            # Try the suggested endpoint first
            suggested_url = f"{RAWG_BASE_URL}/games/{game_data['id']}/suggested"
            print(f"Fetching similar games from: {suggested_url}")
            suggested_response = requests.get(suggested_url, params={"key": settings.RAWG_API_KEY, "page_size": 2}, timeout=10)
            print(f"Similar games response status: {suggested_response.status_code}")
            
            if suggested_response.status_code == 200:
                suggested_data = suggested_response.json()
                results = suggested_data.get("results", [])
                print(f"Similar games from suggested endpoint: {len(results)}")
                
                # If suggested endpoint returns games, use them
                if results:
                    game_obj.similar_games = [
                        {
                            "id": g.get("id"),
                            "name": g.get("name"),
                            "background_image": g.get("background_image"),
                            "rating": g.get("rating"),
                            "genres": g.get("genres", [])[:1]
                        }
                        for g in results[:2]
                    ]
                    print(f"Similar games fetched from suggested: {len(game_obj.similar_games)}")
            
            # Fallback: If suggested endpoint fails or returns empty, search by genre
            if not game_obj.similar_games and game_data.get("genres"):
                print("Suggested endpoint empty, trying genre-based search...")
                # Get all genre IDs from the current game
                genre_ids = [str(g.get("id")) for g in game_data.get("genres", [])]
                
                if genre_ids:
                    # Search for games with the same genres
                    search_url = f"{RAWG_BASE_URL}/games"
                    search_params = {
                        "key": settings.RAWG_API_KEY,
                        "genres": ",".join(genre_ids[:3]),  # Use up to 3 genres for better matching
                        "page_size": 10,  # Get more to filter better
                        "ordering": "-rating",  # Order by rating
                        "metacritic": "70,100"  # Only well-rated games
                    }
                    print(f"Searching with genres: {','.join(genre_ids[:3])}")
                    search_response = requests.get(search_url, params=search_params, timeout=10)
                    
                    if search_response.status_code == 200:
                        search_data = search_response.json()
                        all_results = search_data.get("results", [])
                        
                        # Filter out the current game and games without images
                        similar = [
                            g for g in all_results 
                            if g.get("id") != game_data["id"] 
                            and g.get("background_image")
                            and g.get("rating", 0) > 3.5  # Only games with decent ratings
                        ][:2]
                        
                        game_obj.similar_games = [
                            {
                                "id": g.get("id"),
                                "name": g.get("name"),
                                "background_image": g.get("background_image"),
                                "rating": g.get("rating"),
                                "genres": g.get("genres", [])[:1]
                            }
                            for g in similar
                        ]
                        print(f"Similar games fetched from genre search: {len(game_obj.similar_games)}")
        except Exception as e:
            print(f"Exception fetching similar games: {e}")
            import traceback
            traceback.print_exc()
        
        # Cache result (expire in 1 hour)
        if r:
            try:
                r.setex(cache_key, 3600, game_obj.json())
                print(f"Game cached successfully")
            except Exception as e:
                print(f"Redis cache write failed: {e}")
            
        return game_obj

    except HTTPException:
        raise
    except requests.Timeout as e:
        print(f"Request timeout: {e}")
        raise HTTPException(status_code=504, detail="Request to RAWG API timed out")
    except requests.RequestException as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=502, detail=f"Error communicating with RAWG API: {str(e)}")
    except Exception as e:
        print(f"Unexpected error in get_game_details: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# ============ AUTHENTICATION ENDPOINTS ============

@router.post("/auth/register", response_model=UserResponse)
async def register_user(user_data: UserRegister):
    """Register a new user."""
    # Check if username already exists
    existing_user = database.get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    
    # Hash password
    password_hash = auth.hash_password(user_data.password)
    
    # Create user
    user_id = database.create_user(user_data.username, password_hash)
    if not user_id:
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")
    
    # Generate token
    token = auth.create_access_token(user_id, user_data.username)
    
    return UserResponse(
        user_id=user_id,
        username=user_data.username,
        token=token
    )

@router.post("/auth/login", response_model=UserResponse)
async def login_user(login_data: UserLogin):
    """Login user and return token."""
    # Get user by username
    user = database.get_user_by_username(login_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    
    # Verify password
    if not auth.verify_password(login_data.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    
    # Generate token
    token = auth.create_access_token(user['id'], user['username'])
    
    return UserResponse(
        user_id=user['id'],
        username=user['username'],
        token=token
    )

# ============ FAVORITES ENDPOINTS ============

@router.get("/favorites", response_model=list[FavoriteResponse])
async def get_favorites(current_user: dict = Depends(auth.get_current_user)):
    """Get all favorites for the current user."""
    favorites = database.get_user_favorites(current_user['user_id'])
    return favorites

@router.post("/favorites")
async def add_favorite(favorite: FavoriteGame, current_user: dict = Depends(auth.get_current_user)):
    """Add a game to user's favorites."""
    success = database.add_favorite(
        current_user['user_id'],
        favorite.game_id,
        favorite.game_name,
        favorite.game_image,
        favorite.game_rating
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Jogo já está nos favoritos")
    
    return {"message": "Jogo adicionado aos favoritos"}

@router.delete("/favorites/{game_id}")
async def remove_favorite(game_id: int, current_user: dict = Depends(auth.get_current_user)):
    """Remove a game from user's favorites."""
    success = database.remove_favorite(current_user['user_id'], game_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Jogo não encontrado nos favoritos")
    
    return {"message": "Jogo removido dos favoritos"}

# ============ HARDWARE COMPARISON ENDPOINT ============

@router.post("/compare", response_model=CompareResponse)
async def compare_hardware(compare_data: CompareRequest):
    """Compare user's hardware specs against game requirements."""
    # Fetch game details to get requirements
    try:
        # Search for the game by ID
        detail_url = f"{RAWG_BASE_URL}/games/{compare_data.game_id}"
        response = requests.get(detail_url, params={"key": settings.RAWG_API_KEY}, timeout=10)
        response.raise_for_status()
        game_data = response.json()
        
        # Parse requirements
        platforms = game_data.get("platforms", [])
        pc_requirements = {}
        
        for p in platforms:
            if p.get("platform", {}).get("slug") == "pc":
                pc_requirements = p.get("requirements", {})
                break
        
        parsed_min = parse_requirements(pc_requirements.get("minimum", ""))
        parsed_rec = parse_requirements(pc_requirements.get("recommended", ""))
        
        # Compare specs
        result = comparator.compare_specs(
            user_cpu=compare_data.user_cpu,
            user_gpu=compare_data.user_gpu,
            user_ram=compare_data.user_ram,
            min_cpu=parsed_min.cpu,
            min_gpu=parsed_min.gpu,
            min_ram=parsed_min.ram,
            rec_cpu=parsed_rec.cpu,
            rec_gpu=parsed_rec.gpu,
            rec_ram=parsed_rec.ram
        )
        
        return CompareResponse(**result)
        
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar dados do jogo: {str(e)}")
    except Exception as e:
        print(f"Error in compare_hardware: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao comparar especificações: {str(e)}")

