from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

from chatbot_logic import generate_response
from ai_engine import ask_openclaw

app = FastAPI(
    title="CampusBot Chatbot Service",
    description="Service chatbot utilisant SQLite pour les données officielles et OpenClaw IA pour les questions générales",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_SERVICE_URL = "http://127.0.0.1:8001/api/all"


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "service": "CampusBot Chatbot Service",
        "status": "running",
        "mode": "SQLite official data + OpenClaw IA"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = requests.get(DATA_SERVICE_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        local_response = generate_response(request.message, data)

        if "Je vais utiliser OpenClaw IA" not in local_response:
            return {
                "user_message": request.message,
                "bot_response": local_response,
                "source": "sqlite_database"
            }

        ai_response = ask_openclaw(request.message)

        return {
            "user_message": request.message,
            "bot_response": ai_response,
            "source": "openclaw_ia"
        }

    except requests.exceptions.ConnectionError:
        return {
            "user_message": request.message,
            "bot_response": "Erreur : le Data Service n'est pas lancé. Veuillez démarrer le service de données.",
            "source": "error"
        }

    except Exception as e:
        return {
            "user_message": request.message,
            "bot_response": f"Une erreur est survenue : {str(e)}",
            "source": "error"
        }