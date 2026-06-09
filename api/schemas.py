from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class Emotion(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    NEUTRAL = "neutral"
    THINKING = "thinking"

class GameState(str, Enum):
    IDLE = "idle"
    PLAYING = "playing"
    PAUSED = "paused"
    FINISHED = "finished"

class KiselkaState(BaseModel):
    emotion: Emotion = Emotion.NEUTRAL
    mood: int = 50
    energy: int = 100
    current_game: Optional[str] = None
    message: Optional[str] = None

class GameStartRequest(BaseModel):
    game_type: str
    game_id: str
    config: Optional[Dict[str, Any]] = None

class GameEvent(BaseModel):
    game_id: str
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime = datetime.now()

class DialogueChoice(BaseModel):
    choice_id: int
    text: str
    next_scene: Optional[str] = None

class NovelScene(BaseModel):
    scene_id: str
    background: str
    character: Optional[str] = None
    text: str
    choices: List[DialogueChoice] = []

class Card(BaseModel):
    card_id: str
    name: str
    type: str
    value: int
    description: str

class CardGameState(BaseModel):
    player_hand: List[Card] = []
    opponent_hand: List[Card] = []
    player_health: int = 100
    opponent_health: int = 100
    turn: int = 1