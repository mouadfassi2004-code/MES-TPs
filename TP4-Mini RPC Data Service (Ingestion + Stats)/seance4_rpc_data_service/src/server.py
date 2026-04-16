import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from observability import setup_logger, log_json, record_metric, dump_metrics
from router import MethodRouter
from rpc_protocol import decode_json, encode_json, error_response, success_response, validate_rpc_request
from services import DataStore


logger = setup_logger("rpc.server", "logs/server.log")
store = DataStore()


def handle_ping(params: dict):
    return store.ping()


def handle_ingest_batch(params: dict):
    readings = params.get("readings", [])
    batch_id = params.get("batch_id", "")
    if not isinstance(readings, list):
        raise ValueError("params.readings doit être une liste")
    return store.ingest_batch(batch_id, readings)


def handle_daily_summary(params: dict):
    date_str = params.get("date", "")
    if not isinstance(date_str, str) or not date_str.strip():
        raise ValueError("params.date manquant")
    return store.daily_summary(date_str)


class RPCHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        start = time.monotonic()

        if self.path != "/rpc":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return self._send_rpc(error_response(None, -32700, "Empty body"))

        raw = self.rfile.read(length)

        try:
            data = decode_json(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            return self._send_rpc(error_response(None, -32700, f"Parse error: {e}"))

        valid, message = validate_rpc_request(data)
        rpc_id = data.get("id", "")
        method = data.get("method", "")

        if not valid:
            return self._send_rpc(error_response(rpc_id, -32600, "Invalid request", message))

        try:
            result = self.server.router.dispatch(method, data.get("params", {}))
            response = success_response(rpc_id, result)
            self._send_rpc(response)

            duration = (time.monotonic() - start) * 1000
            record_metric(True, duration)
            dump_metrics()
            log_json(
                logger,
                rpc_id=rpc_id,
                method=method,
                status="success",
                latency_ms=round(duration, 2),
            )
        except KeyError:
            response = error_response(rpc_id, -32601, f"Method not found: {method}")
            self._send_rpc(response)

            duration = (time.monotonic() - start) * 1000
            record_metric(False, duration)
            dump_metrics()
            log_json(
                logger,
                rpc_id=rpc_id,
                method=method,
                status="error",
                code=-32601,
                latency_ms=round(duration, 2),
            )
        except ValueError as e:
            response = error_response(rpc_id, -32602, "Invalid params", str(e))
            self._send_rpc(response)

            duration = (time.monotonic() - start) * 1000
            record_metric(False, duration)
            dump_metrics()
            log_json(
                logger,
                rpc_id=rpc_id,
                method=method,
                status="error",
                code=-32602,
                latency_ms=round(duration, 2),
            )
        except Exception as e:
            response = error_response(rpc_id, -32603, "Internal error", str(e))
            self._send_rpc(response)

            duration = (time.monotonic() - start) * 1000
            record_metric(False, duration)
            dump_metrics()
            log_json(
                logger,
                rpc_id=rpc_id,
                method=method,
                status="error",
                code=-32603,
                latency_ms=round(duration, 2),
            )

    def _send_rpc(self, response_obj):
        body = encode_json(response_obj.to_dict())
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def run_server(host="127.0.0.1", port=8080):
    server = ThreadingHTTPServer((host, port), RPCHandler)
    server.router = MethodRouter()
    server.router.register("health.ping", handle_ping)
    server.router.register("ingest.batch", handle_ingest_batch)
    server.router.register("stats.daily_summary", handle_daily_summary)

    print(f"Serveur RPC démarré sur http://{host}:{port}/rpc")
    server.serve_forever()


if __name__ == "__main__":
    run_server()