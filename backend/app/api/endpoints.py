from fastapi import APIRouter, HTTPException, Query
import requests
from app.core.config import settings
from app.models.schemas import Game, ParsedRequirements
from app.core.parser import parse_requirements
from app.services.rawg_service import rawg_service
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
        try:
            suggested_url = f"{RAWG_BASE_URL}/games/{game_data['id']}/suggested"
            suggested_response = requests.get(suggested_url, params={"key": settings.RAWG_API_KEY, "page_size": 2}, timeout=10)
            if suggested_response.status_code == 200:
                suggested_data = suggested_response.json()
                game_obj.similar_games = [
                    {
                        "id": g.get("id"),
                        "name": g.get("name"),
                        "background_image": g.get("background_image"),
                        "rating": g.get("rating"),
                        "genres": g.get("genres", [])[:1]
                    }
                    for g in suggested_data.get("results", [])[:2]
                ]
                print(f"Similar games fetched: {len(game_obj.similar_games)}")
        except Exception as e:
            print(f"Failed to fetch similar games: {e}")
        
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
