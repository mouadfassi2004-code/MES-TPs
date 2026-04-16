import json
import logging
import os
import socket

from models import SensorReading, IngestRequest
from protocol import build_message, encode_message, recv_ndjson_message


def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("ingestion.client")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler("logs/client.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


logger = setup_logger()


def load_readings(path="data/sample_readings.json"):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [SensorReading.from_dict(item) for item in raw]


def run_client(host="127.0.0.1", port=5000):
    readings = load_readings()

    request_obj = IngestRequest(
        source="station_meteo_01",
        readings=readings,
    )

    message = build_message("ingest_request", request_obj.to_dict())
    request_id = message["request_id"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(10.0)
        sock.connect((host, port))
        logger.info("[%s] Connecté au serveur %s:%d", request_id, host, port)

        sock.sendall(encode_message(message))
        logger.info("[%s] Requête envoyée : %d lectures", request_id, len(readings))

        response = recv_ndjson_message(sock)
        logger.info("[%s] Réponse reçue", request_id)

        os.makedirs("outputs", exist_ok=True)
        with open(f"outputs/client_response_{request_id}.json", "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False, indent=2)

        print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run_client()