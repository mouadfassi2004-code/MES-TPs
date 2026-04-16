import socket
import time
import json

from src.config import HOST, PORT, BUFFER_SIZE, SOCKET_TIMEOUT, SERVER_LOG_FILE
from src.serialization import deserialize_message, serialize_message
from src.validator import validate_message
from src.storage import save_accepted_message
from src.protocol import make_response, make_health_response
from src.logger_setup import setup_logger
from src.metrics import RunMetrics


logger = setup_logger("server_logger", SERVER_LOG_FILE)
metrics = RunMetrics()
processed_request_ids = set()


def process_payload(payload: dict):
    start = time.time()
    metrics.add_received()

    request_id = payload.get("request_id", "UNKNOWN")

    if payload.get("method") == "health.ping":
        response = make_health_response()
        elapsed = time.time() - start
        logger.info(
            f"request_id={request_id} | type=health.ping | decision=accept | "
            f"processing_time_ms={elapsed*1000:.2f}"
        )
        return response

    if request_id in processed_request_ids:
        response = make_response(
            request_id=request_id,
            status="DUPLICATE",
            errors=[],
            message="Duplicate request_id ignored"
        )
        elapsed = time.time() - start
        logger.info(
            f"request_id={request_id} | type=ingest | decision=duplicate | "
            f"processing_time_ms={elapsed*1000:.2f}"
        )
        return response

    valid, errors, normalized = validate_message(payload)

    elapsed = time.time() - start

    if valid:
        processed_request_ids.add(request_id)
        save_accepted_message(normalized)
        metrics.add_accepted(elapsed)

        logger.info(
            f"request_id={request_id} | type=ingest | decision=accept | "
            f"errors=[] | processing_time_ms={elapsed*1000:.2f}"
        )

        return make_response(
            request_id=request_id,
            status="ACCEPTED",
            errors=[],
            message="Message accepted"
        )

    metrics.add_rejected(errors, elapsed)
    logger.info(
        f"request_id={request_id} | type=ingest | decision=reject | "
        f"errors={errors} | processing_time_ms={elapsed*1000:.2f}"
    )

    return make_response(
        request_id=request_id,
        status="REJECTED",
        errors=errors,
        message="Validation failed"
    )


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(SOCKET_TIMEOUT)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            conn.settimeout(SOCKET_TIMEOUT)
            print(f"Connected by {addr}")

            buffer = ""

            try:
                while True:
                    chunk = conn.recv(BUFFER_SIZE)
                    if not chunk:
                        break

                    buffer += chunk.decode("utf-8")

                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        if not line.strip():
                            continue

                        try:
                            payload = deserialize_message(line)
                            response = process_payload(payload)
                        except json.JSONDecodeError:
                            response = make_response(
                                request_id="UNKNOWN",
                                status="REJECTED",
                                errors=["Invalid JSON format"],
                                message="Parsing error"
                            )

                        conn.sendall(serialize_message(response))

            except socket.timeout:
                print("Connection timeout")
            except Exception as e:
                print("Server error:", e)
            finally:
                conn.close()
                metrics.save()

    finally:
        server_socket.close()