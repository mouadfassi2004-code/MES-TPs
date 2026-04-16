import socket
import time
import json
import uuid

from src.config import HOST, PORT, BUFFER_SIZE, SOCKET_TIMEOUT, CLIENT_LOG_FILE
from src.serialization import serialize_message
from src.logger_setup import setup_logger


logger = setup_logger("client_logger", CLIENT_LOG_FILE)


def send_message(payload: dict, retries=2):
    for attempt in range(1, retries + 2):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(SOCKET_TIMEOUT)
                s.connect((HOST, PORT))

                s.sendall(serialize_message(payload))

                buffer = ""
                while True:
                    chunk = s.recv(BUFFER_SIZE)
                    if not chunk:
                        break
                    buffer += chunk.decode("utf-8")
                    if "\n" in buffer:
                        line, _ = buffer.split("\n", 1)
                        response = json.loads(line)
                        logger.info(
                            f"request_id={payload.get('request_id')} | "
                            f"attempt={attempt} | response={response}"
                        )
                        return response

        except Exception as e:
            logger.info(
                f"request_id={payload.get('request_id')} | attempt={attempt} | error={str(e)}"
            )
            time.sleep(1)

    return {
        "request_id": payload.get("request_id"),
        "status": "FAILED",
        "errors": ["All retries failed"],
        "message": ""
    }


def build_sample_messages():
    return [
        {
            "request_id": str(uuid.uuid4()),
            "sensor_id": "S001",
            "site_id": "ZoneA",
            "timestamp": "2026-04-16 10:00:00",
            "temperature": 24.5,
            "humidity": 55,
            "irrigation": "ON",
            "battery": 78
        },
        {
            "request_id": str(uuid.uuid4()),
            "sensor_id": "S002",
            "site_id": "ZoneB",
            "timestamp": "16/04/2026 10:02:00",
            "temperature": "85",
            "humidity": 40,
            "irrigation": "OUI",
            "battery": 50
        },
        {
            "request_id": str(uuid.uuid4()),
            "sensor_id": "",
            "site_id": "ZoneC",
            "timestamp": "2026/04/16 10:03:00",
            "temperature": 21,
            "humidity": 110,
            "irrigation": "NON"
        }
    ]


def run_client():
    health_payload = {
        "request_id": str(uuid.uuid4()),
        "method": "health.ping"
    }
    print(send_message(health_payload))

    messages = build_sample_messages()
    for msg in messages:
        response = send_message(msg)
        print(response)