from api.game_engine import BaseGame
from api.schemas import GameState, GameEvent
import random

class GuessNumberGame(BaseGame):
    def __init__(self, game_id: str):
        super().__init__(game_id)
        self.target_number = 0
        self.attempts = 0
        self.max_attempts = 10
    
    async def start(self, config: Dict[str, Any]) -> Dict[str, Any]:
        self.state = GameState.PLAYING
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = config.get("max_attempts", 10)
        
        return {
            "message": "Я загадала число от 1 до 100! Угадай какое! 🎯",
            "attempts_left": self.max_attempts
        }
    
    async def process_event(self, event: GameEvent) -> Dict[str, Any]:
        if event.event_type == "guess":
            guess = event.data.get("number", 0)
            self.attempts += 1
            
            if guess == self.target_number:
                self.state = GameState.FINISHED
                return {
                    "result": "win",
                    "message": f"Угадал! Это было {self.target_number}! 🎉",
                    "attempts": self.attempts
                }
            elif guess < self.target_number:
                return {
                    "result": "continue",
                    "message": "Больше! ⬆️",
                    "attempts_left": self.max_attempts - self.attempts
                }
            else:
                return {
                    "result": "continue",
                    "message": "Меньше! ⬇️",
                    "attempts_left": self.max_attempts - self.attempts
                }
        
        return {"error": "Unknown event"}
    
    async def get_state(self) -> Dict[str, Any]:
        return {
            "game": "guess_number",
            "state": self.state.value,
            "attempts": self.attempts,
            "attempts_left": self.max_attempts - self.attempts
        }