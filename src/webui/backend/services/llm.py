from __future__ import annotations

from src.core.llm import (
    LlmProviderError,
    fetch_available_models,
    load_explain_llm_settings,
    normalize_llm_settings,
    save_explain_llm_settings,
    test_llm_provider,
)
from src.webui.backend.errors import ServiceError


def load_settings() -> dict:
    return load_explain_llm_settings()


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
    save_explain_llm_settings(current)
    return public_settings()


def require_settings() -> dict:
    settings = load_settings()
    if not settings.get("base_url"):
        raise ServiceError("请先在“大模型配置”页面填写服务地址。")
    if not settings.get("api_key"):
        raise ServiceError("请先在“大模型配置”页面填写访问密钥。")
    if not settings.get("model"):
        raise ServiceError("请先在“大模型配置”页面选择用于生成解释的模型。")
    return settings


def get_llm_config() -> dict:
    return public_settings()


def save_llm_config(payload: dict) -> dict:
    return save_settings(payload)


def _resolve_credentials(payload: dict, action: str) -> dict:
    settings = load_settings()
    base_url = str(payload.get("base_url") or "").strip().rstrip("/")
    saved_base_url = str(settings.get("base_url") or "").strip().rstrip("/")
    api_key = str(payload.get("api_key") or "").strip()
    if not api_key and base_url == saved_base_url:
        api_key = str(settings.get("api_key") or "").strip()

    if not base_url:
        raise ServiceError(f"请先填写服务地址，再{action}。")
    if not api_key:
        raise ServiceError(f"请先填写访问密钥，再{action}。")

    resolved = normalize_llm_settings({**settings, **payload, "base_url": base_url, "api_key": api_key})
    return resolved


def list_llm_models(payload: dict | None = None) -> dict:
    resolved = _resolve_credentials(payload or {}, "获取模型列表")
    try:
        models = fetch_available_models(resolved["base_url"], resolved["api_key"])
    except LlmProviderError as exc:
        message = str(exc)
        if message.startswith("HTTP "):
            raise ServiceError(f"获取模型列表失败（{message}）。请检查服务地址和访问密钥。") from exc
        raise ServiceError("无法连接到模型服务，请检查服务地址和网络连接。") from exc
    return {"models": models}


def test_llm_connection(payload: dict) -> dict:
    resolved = _resolve_credentials(payload, "测试连接")
    if not resolved["model"]:
        raise ServiceError("请先选择解释模型，再测试连接。")

    try:
        return test_llm_provider(
            base_url=resolved["base_url"],
            api_key=resolved["api_key"],
            model=resolved["model"],
            temperature=resolved["temperature"],
        )
    except Exception as exc:
        raise ServiceError(f"连接失败: {exc}") from exc
