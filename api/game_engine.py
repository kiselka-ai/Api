from abc import ABC, abstractmethod
from typing import Dict, Any
from api.schemas import GameState, GameEvent

class BaseGame(ABC):
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.state = GameState.IDLE
        self.config: Dict[str, Any] = {}
    
    @abstractmethod
    async def start(self, config: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def process_event(self, event: GameEvent) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def get_state(self) -> Dict[str, Any]:
        pass
    
    async def pause(self):
        self.state = GameState.PAUSED
    
    async def stop(self):
        self.state = GameState.FINISHED