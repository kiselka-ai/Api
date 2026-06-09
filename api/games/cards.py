from api.game_engine import BaseGame
from api.schemas import GameState, GameEvent, Card, CardGameState
from typing import List
import random

class SimpleCardGame(BaseGame):
    def __init__(self, game_id: str):
        super().__init__(game_id)
        self.game_state = CardGameState()
        self.all_cards = self._create_deck()
    
    def _create_deck(self) -> List[Card]:
        cards = []
        for i in range(20):
            card_type = random.choice(["attack", "defense", "special"])
            value = random.randint(5, 20)
            cards.append(Card(
                card_id=f"card_{i}",
                name=f"Карта {i+1}",
                type=card_type,
                value=value,
                description=f"{card_type} карта с силой {value}"
            ))
        return cards
    
    async def start(self, config: Dict[str, Any]) -> Dict[str, Any]:
        self.state = GameState.PLAYING
        self.game_state = CardGameState()
        self.game_state.player_hand = random.sample(self.all_cards, 5)
        self.game_state.opponent_hand = random.sample(self.all_cards, 5)
        return self.game_state.dict()
    
    async def process_event(self, event: GameEvent) -> Dict[str, Any]:
        if event.event_type == "play_card":
            card_id = event.data.get("card_id")
            card = next((c for c in self.game_state.player_hand if c.card_id == card_id), None)
            
            if card:
                if card.type == "attack":
                    self.game_state.opponent_health -= card.value
                    message = f"Атака на {card.value} урона! ⚔️"
                elif card.type == "defense":
                    self.game_state.player_health += card.value
                    message = f"Восстановлено {card.value} здоровья! 🛡️"
                else:
                    effect = random.choice(["heal", "damage"])
                    if effect == "heal":
                        self.game_state.player_health += 15
                        message = "Спецкарта! +15 здоровья! ✨"
                    else:
                        self.game_state.opponent_health -= 15
                        message = "Спецкарта! -15 противнику! ✨"
                
                self.game_state.player_hand = [c for c in self.game_state.player_hand if c.card_id != card_id]
                
                if self.game_state.opponent_hand:
                    opponent_card = random.choice(self.game_state.opponent_hand)
                    self.game_state.player_health -= opponent_card.value
                    self.game_state.opponent_hand.remove(opponent_card)
                    message += f" Противник атаковал на {opponent_card.value}! 😱"
                
                self.game_state.turn += 1
                
                if self.game_state.opponent_health <= 0:
                    self.state = GameState.FINISHED
                    message += " Победа! 🎉"
                elif self.game_state.player_health <= 0:
                    self.state = GameState.FINISHED
                    message += " Поражение... 😢"
                
                return {"message": message, "state": self.game_state.dict()}
        
        return {"error": "Unknown event"}
    
    async def get_state(self) -> Dict[str, Any]:
        return self.game_state.dict()