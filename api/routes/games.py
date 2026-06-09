from fastapi import APIRouter, HTTPException
from api.schemas import GameStartRequest, GameEvent
from api.games.mini_game import GuessNumberGame
from api.games.novel import SimpleNovel
from api.games.cards import SimpleCardGame

router = APIRouter(prefix="/games", tags=["games"])

active_games = {}

@router.post("/start")
async def start_game(request: GameStartRequest):
    game_id = request.game_id
    
    if game_id in active_games:
        raise HTTPException(status_code=400, detail="Game already running")
    
    if request.game_type == "mini":
        game = GuessNumberGame(game_id)
    elif request.game_type == "novel":
        game = SimpleNovel(game_id)
    elif request.game_type == "card":
        game = SimpleCardGame(game_id)
    else:
        raise HTTPException(status_code=400, detail="Unknown game type")
    
    result = await game.start(request.config or {})
    active_games[game_id] = game
    
    return {"status": "started", "game_id": game_id, "data": result}

@router.post("/{game_id}/event")
async def send_event(game_id: str, event: GameEvent):
    if game_id not in active_games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = active_games[game_id]
    result = await game.process_event(event)
    
    if game.state.value == "finished":
        del active_games[game_id]
    
    return result

@router.get("/{game_id}/state")
async def get_game_state(game_id: str):
    if game_id not in active_games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = active_games[game_id]
    return await game.get_state()

@router.delete("/{game_id}")
async def stop_game(game_id: str):
    if game_id not in active_games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = active_games[game_id]
    await game.stop()
    del active_games[game_id]
    
    return {"status": "stopped"}