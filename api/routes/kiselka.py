from fastapi import APIRouter
from api.schemas import KiselkaState, Emotion

router = APIRouter(prefix="/kiselka", tags=["kiselka"])

kiselka_state = KiselkaState()

@router.get("/state")
async def get_kiselka_state():
    return kiselka_state

@router.post("/emotion")
async def set_emotion(emotion: Emotion):
    kiselka_state.emotion = emotion
    
    messages = {
        Emotion.HAPPY: "Ура! Я так рада! 😊",
        Emotion.SAD: "Мне грустно... 😢",
        Emotion.ANGRY: "Я злюсь! 😤",
        Emotion.SURPRISED: "Ого! Не ожидала! 😮",
        Emotion.THINKING: "Хм, дай подумать... 🤔",
        Emotion.NEUTRAL: "Ну ладно... 😐"
    }
    
    kiselka_state.message = messages[emotion]
    return {"status": "ok", "message": kiselka_state.message}

@router.post("/mood")
async def set_mood(mood: int):
    kiselka_state.mood = max(0, min(100, mood))
    return {"status": "ok", "mood": kiselka_state.mood}