from api.game_engine import BaseGame
from api.schemas import GameState, GameEvent, NovelScene, DialogueChoice
from typing import Dict, List

class SimpleNovel(BaseGame):
    def __init__(self, game_id: str):
        super().__init__(game_id)
        self.current_scene = "start"
        self.scenes: Dict[str, NovelScene] = {}
        self._init_scenes()
    
    def _init_scenes(self):
        self.scenes = {
            "start": NovelScene(
                scene_id="start",
                background="classroom.jpg",
                character="kiselka",
                text="Привет! Я Киселька! Добро пожаловать! 💕",
                choices=[
                    DialogueChoice(choice_id=1, text="Привет!", next_scene="greeting"),
                    DialogueChoice(choice_id=2, text="Расскажи о себе", next_scene="about")
                ]
            ),
            "greeting": NovelScene(
                scene_id="greeting",
                background="classroom.jpg",
                character="kiselka",
                text="Рада тебя видеть! Давай дружить! 💖",
                choices=[
                    DialogueChoice(choice_id=1, text="Давай!", next_scene="friends"),
                    DialogueChoice(choice_id=2, text="Пока", next_scene="end")
                ]
            ),
            "about": NovelScene(
                scene_id="about",
                background="room.jpg",
                character="kiselka",
                text="Я виртуальная стримерша! Люблю аниме и игры! 🎮",
                choices=[
                    DialogueChoice(choice_id=1, text="Круто!", next_scene="friends"),
                    DialogueChoice(choice_id=2, text="Пока", next_scene="end")
                ]
            ),
            "friends": NovelScene(
                scene_id="friends",
                background="park.jpg",
                character="kiselka",
                text="Ура! Теперь мы друзья! 🎉",
                choices=[
                    DialogueChoice(choice_id=1, text="Давай играть!", next_scene="end"),
                    DialogueChoice(choice_id=2, text="Пока", next_scene="end")
                ]
            ),
            "end": NovelScene(
                scene_id="end",
                background="sunset.jpg",
                character="kiselka",
                text="Спасибо что поиграл! Возвращайся! 👋",
                choices=[]
            )
        }
    
    async def start(self, config: Dict[str, Any]) -> Dict[str, Any]:
        self.state = GameState.PLAYING
        self.current_scene = "start"
        return self.scenes["start"].dict()
    
    async def process_event(self, event: GameEvent) -> Dict[str, Any]:
        if event.event_type == "choice":
            choice_id = event.data.get("choice_id")
            scene = self.scenes.get(self.current_scene)
            
            if scene:
                for choice in scene.choices:
                    if choice.choice_id == choice_id:
                        self.current_scene = choice.next_scene
                        next_scene = self.scenes.get(self.current_scene)
                        
                        if self.current_scene == "end":
                            self.state = GameState.FINISHED
                        
                        return next_scene.dict() if next_scene else {"error": "Scene not found"}
            
            return {"error": "Invalid choice"}
        
        return {"error": "Unknown event"}
    
    async def get_state(self) -> Dict[str, Any]:
        scene = self.scenes.get(self.current_scene)
        return scene.dict() if scene else {}