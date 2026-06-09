# 🎮 Kiselka API

**Единая система управления для мини-игр, визуальных новелл и карточных игр с интеграцией AI-аватара Киселька.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 О проекте

**Kiselka API** — это REST API сервер, который предоставляет единый интерфейс для управления различными типами игр и интеграции с AI-аватаром Киселька. 

Проект построен на принципе **единой точки входа** — все игры (мини-игры, визуальные новеллы, карточные игры) управляются через одинаковый API, что позволяет легко интегрировать их с фронтендом, стриминговыми платформами (Twitch, YouTube) или AI-ассистентом.

### 🎯 Основные возможности

- 🎲 **Мини-игры** — простые игры (угадай число и др.)
- 📖 **Визуальные новеллы** — интерактивные истории с выборами
- 🃏 **Карточные игры** — пошаговые карточные баталии
- 🎭 **Управление AI-аватаром** — эмоции, настроение, состояние
- 🔌 **REST API** — стандартный интерфейс для любых клиентов
- 📚 **Автодокументация** — Swagger UI из коробки
- ⚡ **Асинхронность** — FastAPI + asyncio
- 🧩 **Расширяемость** — легко добавить новые игры

---

## 🛠️ Стек технологий

| Технология | Версия | Назначение |
|------------|--------|------------|
| **Python** | 3.10+ | Основной язык |
| **FastAPI** | 0.100+ | Web-фреймворк |
| **Pydantic** | 2.0+ | Валидация данных |
| **Uvicorn** | 0.23+ | ASGI сервер |

---

## 📦 Установка

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/kiselka-api.git
cd kiselka-api
```

### 2. Создайте виртуальное окружение

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Содержимое `requirements.txt`

```txt
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
```

---

## 🚀 Запуск

### Режим разработки (с автоперезагрузкой)

```bash
python main.py
```

### Режим продакшена

```bash
uvicorn api.server:app --host 0.0.0.0 --port 8000 --workers 4
```

После запуска API доступен по адресу:
- **API**: http://localhost:8000
- **Документация (Swagger)**: http://localhost:8000/docs
- **Документация (ReDoc)**: http://localhost:8000/redoc

---

## 📚 Документация API

### 🎭 Управление Киселькой

#### Получить состояние Кисельки

```http
GET /kiselka/state
```

**Ответ:**
```json
{
  "emotion": "neutral",
  "mood": 50,
  "energy": 100,
  "current_game": null,
  "message": null
}
```

#### Изменить эмоцию Кисельки

```http
POST /kiselka/emotion
Content-Type: application/json

"happy"
```

**Доступные эмоции:**
- `happy` — радость 😊
- `sad` — грусть 😢
- `angry` — злость 😤
- `surprised` — удивление 😮
- `thinking` — раздумье 🤔
- `neutral` — нейтральное 😐

#### Изменить настроение

```http
POST /kiselka/mood
Content-Type: application/json

75
```

**Параметры:** значение от 0 до 100

---

### 🎮 Управление играми

#### Запустить новую игру

```http
POST /games/start
Content-Type: application/json

{
  "game_type": "mini",
  "game_id": "guess_1",
  "config": {
    "max_attempts": 10
  }
}
```

**Типы игр (`game_type`):**
- `mini` — мини-игры (угадай число)
- `novel` — визуальные новеллы
- `card` — карточные игры

**Ответ:**
```json
{
  "status": "started",
  "game_id": "guess_1",
  "data": {
    "message": "Я загадала число от 1 до 100! Угадай какое! 🎯",
    "attempts_left": 10
  }
}
```

#### Отправить событие в игру

```http
POST /games/{game_id}/event
Content-Type: application/json

{
  "game_id": "guess_1",
  "event_type": "guess",
  "data": {
    "number": 50
  }
}
```

**Типы событий по играм:**

| Игра | `event_type` | `data` |
|------|--------------|--------|
| mini | `guess` | `{"number": 50}` |
| novel | `choice` | `{"choice_id": 1}` |
| card | `play_card` | `{"card_id": "card_1"}` |

#### Получить состояние игры

```http
GET /games/{game_id}/state
```

#### Остановить игру

```http
DELETE /games/{game_id}
```

---

## 🎯 Примеры использования

### Пример 1: Мини-игра "Угадай число"

```bash
# 1. Запускаем игру
curl -X POST http://localhost:8000/games/start \
  -H "Content-Type: application/json" \
  -d '{"game_type": "mini", "game_id": "guess_1"}'

# 2. Делаем попытку
curl -X POST http://localhost:8000/games/guess_1/event \
  -H "Content-Type: application/json" \
  -d '{"game_id": "guess_1", "event_type": "guess", "data": {"number": 50}}'

# 3. Проверяем состояние
curl http://localhost:8000/games/guess_1/state
```

### Пример 2: Визуальная новелла

```bash
# 1. Запускаем новеллу
curl -X POST http://localhost:8000/games/start \
  -H "Content-Type: application/json" \
  -d '{"game_type": "novel", "game_id": "novel_1"}'

# 2. Делаем выбор
curl -X POST http://localhost:8000/games/novel_1/event \
  -H "Content-Type: application/json" \
  -d '{"game_id": "novel_1", "event_type": "choice", "data": {"choice_id": 1}}'
```

### Пример 3: Карточная игра

```bash
# 1. Запускаем игру
curl -X POST http://localhost:8000/games/start \
  -H "Content-Type: application/json" \
  -d '{"game_type": "card", "game_id": "card_1"}'

# 2. Играем картой
curl -X POST http://localhost:8000/games/card_1/event \
  -H "Content-Type: application/json" \
  -d '{"game_id": "card_1", "event_type": "play_card", "data": {"card_id": "card_0"}}'
```

### Пример 4: Управление эмоциями Кисельки

```bash
# Делаем Кисельку счастливой
curl -X POST http://localhost:8000/kiselka/emotion \
  -H "Content-Type: application/json" \
  -d '"happy"'

# Устанавливаем настроение
curl -X POST http://localhost:8000/kiselka/mood \
  -H "Content-Type: application/json" \
  -d '90'
```

---

## 📁 Структура проекта

```
kiselka-api/
├── api/
│   ├── __init__.py
│   ├── server.py           # FastAPI приложение
│   ├── schemas.py          # Pydantic модели
│   ├── game_engine.py      # Базовый класс игры
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── kiselka.py      # Роуты управления Киселькой
│   │   └── games.py        # Роуты управления играми
│   └── games/
│       ├── __init__.py
│       ├── mini_game.py    # Мини-игры
│       ├── novel.py        # Визуальные новеллы
│       └── cards.py        # Карточные игры
├── main.py                 # Точка входа
├── requirements.txt        # Зависимости
└── README.md               # Документация
```

---

## 🧩 Как добавить новую игру

### 1. Создайте класс игры в `api/games/`

```python
# api/games/my_game.py
from api.game_engine import BaseGame
from api.schemas import GameState, GameEvent

class MyAwesomeGame(BaseGame):
    def __init__(self, game_id: str):
        super().__init__(game_id)
        self.score = 0
    
    async def start(self, config: dict) -> dict:
        self.state = GameState.PLAYING
        return {"message": "Игра началась!"}
    
    async def process_event(self, event: GameEvent) -> dict:
        # Ваша логика
        return {"result": "ok"}
    
    async def get_state(self) -> dict:
        return {"score": self.score, "state": self.state.value}
```

### 2. Зарегистрируйте игру в `api/routes/games.py`

```python
from api.games.my_game import MyAwesomeGame

@router.post("/start")
async def start_game(request: GameStartRequest):
    # ... существующий код ...
    
    elif request.game_type == "my_game":
        game = MyAwesomeGame(game_id)
    
    # ...
```

Готово! 🎉

---

## 🔗 Интеграция с Киселькой (AI-аватаром)

API можно интегрировать с основным проектом Kiselka (AI-аватар):

```python
import httpx

class KiselkaAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    async def set_emotion(self, emotion: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/kiselka/emotion",
                json=emotion
            )
            return response.json()
    
    async def start_game(self, game_type: str, game_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/games/start",
                json={
                    "game_type": game_type,
                    "game_id": game_id
                }
            )
            return response.json()
```

---

## 🗺️ Roadmap

### ✅ v1.0 (Текущая версия)
- [x] Базовый API
- [x] Мини-игра "Угадай число"
- [x] Простая визуальная новелла
- [x] Карточная игра
- [x] Управление эмоциями Кисельки

### 🚧 v1.1 (Планируется)
- [ ] WebSocket для real-time обновлений
- [ ] Сохранение прогресса игр в БД
- [ ] Больше мини-игр (викторина, память)
- [ ] Система достижений

### 🎯 v2.0 (В планах)
- [ ] Интеграция с Twitch (зрители влияют на игры)
- [ ] Мультиплеер (несколько игроков)
- [ ] Редактор визуальных новелл
- [ ] Кастомные карточные колоды
- [ ] Интеграция с VTube Studio

---

## 🤝 Вклад в проект

Pull requests приветствуются! Для крупных изменений сначала откройте issue, чтобы обсудить что вы хотите изменить.

---

## 📄 Лицензия

MIT License — используйте свободно!

---

---

## 💖 Благодарности

- [FastAPI](https://fastapi.tiangolo.com/) — за отличный фреймворк
  [Подкинуть монетку](https://www.donationalerts.com/r/prosto_lino4ka)
- Всем кто поддерживает проект!

---

<p align="center">
  Сделано с 💖 для сообщества стримеров и геймеров
</p>
