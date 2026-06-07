from __future__ import annotations

import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import yaml

from src.config import resolve_path
from src.explain.llm_client import OpenAICompatibleClient

LLM_CONFIG_PATH = resolve_path("configs/llm.local.yaml")
DEFAULT_LLM_SETTINGS = {
    "base_url": "",
    "api_key": "",
    "model": "",
    "temperature": 0.2,
}


class LlmProviderError(RuntimeError):
    pass


def normalize_llm_settings(settings: dict) -> dict:
    normalized = dict(DEFAULT_LLM_SETTINGS)
    normalized.update({key: value for key, value in settings.items() if key in DEFAULT_LLM_SETTINGS})
    normalized["base_url"] = str(normalized.get("base_url", "")).strip().rstrip("/")
    normalized["model"] = str(normalized.get("model", "")).strip()
    normalized["api_key"] = str(normalized.get("api_key", "")).strip()
    normalized["temperature"] = float(normalized.get("temperature", 0.2))
    return normalized


def load_explain_llm_settings() -> dict:
    with LLM_CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return normalize_llm_settings(data)


def save_explain_llm_settings(settings: dict) -> dict:
    normalized = normalize_llm_settings(settings)
    LLM_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LLM_CONFIG_PATH.open("w", encoding="utf-8") as f:
        yaml.safe_dump(normalized, f, allow_unicode=True, sort_keys=False)
    return normalized


def fetch_available_models(base_url: str, api_key: str, timeout: int = 20) -> list[str]:
    request = Request(f"{base_url.rstrip('/')}/models", headers={"Authorization": f"Bearer {api_key}"})
    try:
        with urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise LlmProviderError(f"HTTP {exc.code}") from exc
    except URLError as exc:
        raise LlmProviderError("connection failed") from exc

    models = []
    for item in body.get("data", []):
        model_id = item.get("id")
        if model_id:
            models.append(str(model_id))
    return sorted(models)


def test_llm_provider(base_url: str, api_key: str, model: str, temperature: float) -> dict:
    start_time = time.perf_counter()
    client = OpenAICompatibleClient(model=model, base_url=base_url, api_key=api_key)
    message = client.complete(system="你是一名测试助手。", user="你是什么模型？", temperature=temperature)
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return {"message": message, "elapsed_ms": elapsed_ms}
