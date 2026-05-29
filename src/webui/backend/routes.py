from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

from src.webui.backend import services
from src.webui.backend.errors import ServiceError


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self._json(200, services.health())
            return
        if path == "/llm/config":
            self._json(200, services.get_llm_config())
            return
        if path == "/llm/models":
            try:
                self._json(200, services.list_llm_models())
            except ServiceError as exc:
                self._json(400, {"error": str(exc)})
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path not in ("/predict", "/explain", "/llm/config", "/llm/models"):
            self._json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            if path == "/llm/config":
                result = services.save_llm_config(payload)
            elif path == "/llm/models":
                result = services.list_llm_models(payload)
            else:
                result = services.predict(payload.get("text", ""), explain=path == "/explain")
            self._json(200, result)
        except ServiceError as exc:
            self._json(400, {"error": str(exc)})
        except Exception as exc:
            self._json(500, {"error": str(exc)})

    def _json(self, status: int, data: dict) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args) -> None:
        return
