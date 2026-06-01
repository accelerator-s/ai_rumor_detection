from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

from src.webui.backend import services
from src.webui.backend.errors import ServiceError

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
RESOURCES_DIR = FRONTEND_DIR / "resources"

_MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".svg": "image/svg+xml; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".ico": "image/x-icon",
}


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
        if path in ("/favicon.ico", "/favicon.svg"):
            self._static("favicon.svg", root=RESOURCES_DIR)
            return
        if path in ("/", "/index.html"):
            self._static("index.html", root=FRONTEND_DIR)
            return
        if path == "/app.js":
            self._static("app.js", root=FRONTEND_DIR)
            return
        if path.startswith(("/core/", "/components/")):
            self._static(path.lstrip("/"), root=FRONTEND_DIR)
            return
        if path.startswith("/resources/"):
            self._static(path[len("/resources/") :], root=RESOURCES_DIR)
            return
        self._json(404, {"error": "not found"})

    def do_HEAD(self) -> None:
        path = urlparse(self.path).path
        if path in ("/favicon.ico", "/favicon.svg"):
            self._static("favicon.svg", root=RESOURCES_DIR, head_only=True)
            return
        if path in ("/", "/index.html"):
            self._static("index.html", root=FRONTEND_DIR, head_only=True)
            return
        if path == "/app.js":
            self._static("app.js", root=FRONTEND_DIR, head_only=True)
            return
        if path.startswith(("/core/", "/components/")):
            self._static(path.lstrip("/"), root=FRONTEND_DIR, head_only=True)
            return
        if path.startswith("/resources/"):
            self._static(path[len("/resources/") :], root=RESOURCES_DIR, head_only=True)
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path not in ("/predict", "/explain", "/batch", "/llm/config", "/llm/models", "/llm/test"):
            self._json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            if path == "/llm/config":
                result = services.save_llm_config(payload)
            elif path == "/llm/models":
                result = services.list_llm_models(payload)
            elif path == "/llm/test":
                result = services.test_llm_connection(payload)
            elif path == "/batch":
                result = services.batch_predict(payload)
            else:
                result = services.predict(payload.get("text", ""), event=payload.get("event"), explain=path == "/explain")
            self._json(200, result)
        except ServiceError as exc:
            self._json(400, {"error": str(exc)})
        except Exception as exc:
            message = str(exc).strip() or "服务处理请求失败，请检查后端日志。"
            self._json(500, {"error": message})

    def _static(
        self, rel: str, root: Path = FRONTEND_DIR, head_only: bool = False
    ) -> None:
        try:
            target = (root / rel).resolve()
        except (OSError, ValueError):
            self._json(404, {"error": "not found"})
            return
        if target != root and root not in target.parents:
            self._json(403, {"error": "forbidden"})
            return
        if not target.is_file():
            self._json(404, {"error": "not found"})
            return
        body = target.read_bytes()
        self.send_response(200)
        self.send_header(
            "Content-Type", _MIME.get(target.suffix, "application/octet-stream")
        )
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def _json(self, status: int, data: dict) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args) -> None:
        return
