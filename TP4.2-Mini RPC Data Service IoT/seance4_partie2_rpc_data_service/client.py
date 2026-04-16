import json
import time
import urllib.request
import urllib.error

from rpc_protocol import build_request


class RpcClient:
    def __init__(self, url: str, default_timeout: float = 5.0, max_retries: int = 2):
        self.url = url.rstrip("/")
        self.default_timeout = default_timeout
        self.max_retries = max_retries

    def call(self, method: str, params: dict = None):
        req_obj = build_request(method, params or {})
        rpc_id = req_obj["id"]
        payload = json.dumps(req_obj).encode("utf-8")

        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(
                    self.url + "/rpc",
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                start = time.monotonic()
                with urllib.request.urlopen(req, timeout=self.default_timeout) as resp:
                    raw = resp.read()
                duration = round((time.monotonic() - start) * 1000, 2)
                print(json.dumps({
                    "rpc_id": rpc_id,
                    "method": method,
                    "status": "received",
                    "latency_ms": duration,
                    "attempt": attempt + 1
                }, ensure_ascii=False))
                return json.loads(raw.decode("utf-8"))

            except (urllib.error.URLError, TimeoutError) as e:
                if attempt >= self.max_retries:
                    break
                delay = 2 ** attempt
                print(json.dumps({
                    "rpc_id": rpc_id,
                    "method": method,
                    "status": "retry",
                    "attempt": attempt + 1,
                    "delay_s": delay,
                    "error": str(e)
                }, ensure_ascii=False))
                time.sleep(delay)

        raise RuntimeError(f"Échec RPC après {self.max_retries + 1} tentatives")