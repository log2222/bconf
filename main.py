from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
import os

app = FastAPI()

# Разрешаем CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

@app.get("/components")
def get_components() -> Dict:
    """Возвращает список комплектующих по категориям."""
    with open(os.path.join(DATA_DIR, 'components.json'), encoding='utf-8') as f:
        return json.load(f)

@app.get("/presets")
def get_presets() -> List[Dict]:
    """Возвращает список типовых конфигов."""
    with open(os.path.join(DATA_DIR, 'presets.json'), encoding='utf-8') as f:
        return json.load(f) 