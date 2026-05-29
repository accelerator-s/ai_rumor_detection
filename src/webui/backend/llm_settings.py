from __future__ import annotations

import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import yaml

from src.config import resolve_path
from src.webui.backend.errors import ServiceError


CONFIG_PATH = resolve_path("configs/webui_llm.local.yaml")
DEFAULTS = {
    "base_url": "",
    "api_key": "",
    "model": "",
    "temperature": 0.2,
}


def load_settings() -> dict:
    if not CONFIG_PATH.exists():
        return dict(DEFAULTS)
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    settings = dict(DEFAULTS)
    settings.update({key: value for key, value in data.items() if key in DEFAULTS})
    return settings


def public_settings() -> dict:
    settings = load_settings()
    return {
        "base_url": settings["base_url"],
        "model": settings["model"],
        "temperature": settings["temperature"],
        "has_api_key": bool(settings["api_key"]),
    }


def save_settings(payload: dict) -> dict:
    current = load_settings()
    for key in ("base_url", "api_key", "model", "temperature"):
        if key in payload:
            current[key] = payload[key]
    current["base_url"] = str(current.get("base_url", "")).strip().rstrip("/")
    current["model"] = str(current.get("model", "")).strip()
    current["api_key"] = str(current.get("api_key", "")).strip()
    current["temperature"] = float(current.get("temperature", 0.2))

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        yaml.safe_dump(current, f, allow_unicode=True, sort_keys=False)
    return public_settings()


def require_settings() -> dict:
    settings = load_settings()
    if not settings.get("base_url"):
        raise ServiceError("Set LLM base_url in WebUI first.")
    if not settings.get("api_key"):
        raise ServiceError("Set LLM api_key in WebUI first.")
    if not settings.get("model"):
        raise ServiceError("Select an LLM model in WebUI first.")
    return settings


def fetch_models(base_url: str | None = None, api_key: str | None = None) -> list[str]:
    settings = load_settings()
    url = (base_url or settings.get("base_url") or "").strip().rstrip("/")
    token = api_key if api_key is not None else settings.get("api_key", "")
    if not url:
        raise ServiceError("Set LLM base_url before fetching models.")
    if not token:
        raise ServiceError("Set LLM api_key before fetching models.")

    request = Request(f"{url}/models", headers={"Authorization": f"Bearer {token}"})
    try:
        with urlopen(request, timeout=20) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise ServiceError(f"Model list request failed: HTTP {exc.code}") from exc
    except URLError as exc:
        raise ServiceError(f"Model list request failed: {exc.reason}") from exc

    models = []
    for item in body.get("data", []):
        model_id = item.get("id")
        if model_id:
            models.append(str(model_id))
    return sorted(models)
