import json
import os
from src.config import DATA_FILE


def ensure_data_file():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            pass


def save_accepted_message(message: dict):
    ensure_data_file()
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(message) + "\n")