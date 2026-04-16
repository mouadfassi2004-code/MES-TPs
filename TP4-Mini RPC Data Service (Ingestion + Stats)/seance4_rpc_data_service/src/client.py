import json
import time
import urllib.request
import urllib.error

from observability import setup_logger, log_json
from rpc_protocol import build_request


logger = setup_logger("rpc.client", "logs/client.log")


class RpcClient:
    def __init__(self, endpoint: str, timeout: float = 3.0, max_retries: int = 3):
        self.endpoint = endpoint
        self.timeout = timeout
        self.max_retries = max_retries

    def call(self, method: str, params: dict):
        request_obj = build_request(method, params)
        rpc_id = request_obj.id
        payload = json.dumps(request_obj.to_dict()).encode("utf-8")

        for attempt in range(self.max_retries):
            try:
                req = urllib.request.Request(
                    self.endpoint,
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )

                start = time.monotonic()
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    raw = resp.read()
                duration = (time.monotonic() - start) * 1000

                response = json.loads(raw.decode("utf-8"))
                log_json(
                    logger,
                    rpc_id=rpc_id,
                    method=method,
                    status="received",
                    latency_ms=round(duration, 2),
                    attempt=attempt + 1,
                )
                return response

            except (urllib.error.URLError, TimeoutError) as e:
                delay = 2 ** attempt
                log_json(
                    logger,
                    rpc_id=rpc_id,
                    method=method,
                    status="retry",
                    attempt=attempt + 1,
                    delay_s=delay,
                    error=str(e),
                )
                time.sleep(delay)

        raise RuntimeError(f"Échec RPC après {self.max_retries} tentatives")