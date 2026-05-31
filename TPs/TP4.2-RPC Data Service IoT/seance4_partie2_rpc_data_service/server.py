import json
import logging
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from router import MethodRouter
from rpc_protocol import validate_rpc_request, build_response, build_error_response
from services import DataStore


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(message)s",
)

logger = logging.getLogger("rpc_server")

store = DataStore()
router = MethodRouter()
router.register("health.ping", store.health_ping)
router.register("ingest.batch", store.ingest_batch)
router.register("stats.daily_summary", store.daily_summary)
router.register("stats.top_sensors", store.top_sensors)


class RPCHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        start = time.monotonic()

        if self.path != "/rpc":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        parsed, error = validate_rpc_request(raw_body)
        if error is not None:
            return self._send_json(error)

        rpc_id = parsed["id"]
        method = parsed["method"]
        params = parsed["params"]

        try:
            result = router.dispatch(method, params)
            response = build_response(rpc_id, result)
            duration_ms = round((time.monotonic() - start) * 1000, 2)
            logger.info(json.dumps({
                "rpc_id": rpc_id,
                "method": method,
                "status": "ok",
                "latency_ms": duration_ms
            }, ensure_ascii=False))
            return self._send_json(response)

        except KeyError:
            response = build_error_response(rpc_id, -32601, "Method not found", method)
            return self._send_json(response)

        except ValueError as e:
            response = build_error_response(rpc_id, -32602, "Invalid params", str(e))
            return self._send_json(response)

        except Exception as e:
            logger.exception("Erreur interne")
            response = build_error_response(rpc_id, -32603, "Internal error", str(e))
            return self._send_json(response)

    def _send_json(self, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def run():
    server = ThreadingHTTPServer(("127.0.0.1", 8080), RPCHandler)
    print("Serveur RPC démarré sur http://127.0.0.1:8080/rpc")
    server.serve_forever()


if __name__ == "__main__":
    run()