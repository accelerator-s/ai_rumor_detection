from __future__ import annotations

import json
from urllib.request import Request, urlopen


class BackendClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000") -> None:
        self.base_url = base_url.rstrip("/")

    def health(self) -> dict:
        with urlopen(f"{self.base_url}/health", timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    def llm_config(self) -> dict:
        with urlopen(f"{self.base_url}/llm/config", timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    def save_llm_config(self, config: dict) -> dict:
        return self._post("/llm/config", config, timeout=20)

    def models(self, base_url: str, api_key: str) -> list[str]:
        result = self._post("/llm/models", {"base_url": base_url, "api_key": api_key}, timeout=30)
        return result.get("models", [])

    def explain(self, text: str) -> dict:
        return self._post("/explain", {"text": text}, timeout=120)

    def _post(self, path: str, payload: dict, timeout: int) -> dict:
        body = json.dumps(payload).encode("utf-8")
        request = Request(
            f"{self.base_url}{path}",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
