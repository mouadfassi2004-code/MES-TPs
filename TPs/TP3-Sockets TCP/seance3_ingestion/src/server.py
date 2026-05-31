import json
import logging
import os
import socket

from models import IngestRequest, IngestResponse
from protocol import build_message, encode_message, recv_ndjson_message
from validators import validate_reading


def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("ingestion.server")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler("logs/server.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


logger = setup_logger()


def process_ingest_request(request: IngestRequest):
    accepted = 0
    rejected = 0
    all_errors = []

    for reading in request.readings:
        errors = validate_reading(reading)
        if errors:
            rejected += 1
            all_errors.extend(errors)
        else:
            accepted += 1

    if rejected == 0:
        status = "ok"
    elif accepted > 0:
        status = "partial"
    else:
        status = "error"

    return IngestResponse(
        status=status,
        accepted_count=accepted,
        rejected_count=rejected,
        errors=all_errors,
    )


def save_response_json(request_id: str, response_dict: dict):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", f"response_{request_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(response_dict, f, ensure_ascii=False, indent=2)


def run_server(host="127.0.0.1", port=5000):
    logger.info("Serveur démarré sur %s:%d", host, port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((host, port))
        server_sock.listen(5)

        while True:
            conn, addr = server_sock.accept()
            with conn:
                conn.settimeout(10.0)
                logger.info("Connexion acceptée depuis %s:%d", addr[0], addr[1])

                try:
                    message = recv_ndjson_message(conn)
                    if message is None:
                        logger.warning("Connexion fermée sans message")
                        continue

                    request_id = message.get("request_id", "unknown")
                    msg_type = message.get("type", "")

                    logger.info("[%s] Message reçu : type=%s", request_id, msg_type)

                    if msg_type != "ingest_request":
                        error_response = build_message(
                            "error",
                            {"message": "type de message non supporté"},
                            request_id=request_id
                        )
                        conn.sendall(encode_message(error_response))
                        logger.error("[%s] Type invalide reçu", request_id)
                        continue

                    payload = message.get("payload", {})
                    ingest_request = IngestRequest.from_dict(payload)
                    response_obj = process_ingest_request(ingest_request)

                    response_msg = build_message(
                        "ingest_response",
                        response_obj.to_dict(),
                        request_id=request_id
                    )

                    conn.sendall(encode_message(response_msg))
                    save_response_json(request_id, response_msg)

                    logger.info(
                        "[%s] Réponse envoyée : accepted=%d, rejected=%d",
                        request_id,
                        response_obj.accepted_count,
                        response_obj.rejected_count,
                    )

                except socket.timeout:
                    logger.error("Timeout côté serveur")
                except Exception as e:
                    logger.exception("Erreur serveur : %s", e)


if __name__ == "__main__":
    run_server()