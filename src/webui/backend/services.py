from __future__ import annotations

from src.webui.backend.errors import ServiceError
from src.webui.backend import llm_settings
from src.webui.backend.state import state


def health() -> dict:
    return {
        "ok": state.pipeline is not None,
        "error": state.error,
        "llm": llm_settings.public_settings(),
    }


def predict(text: str, explain: bool = True) -> dict:
    if state.pipeline is None:
        raise ServiceError(state.error or "Pipeline is not loaded.")
    if not text.strip():
        raise ServiceError("Text is required.")
    llm_config = llm_settings.require_settings() if explain else None
    return state.pipeline.predict(text, explain=explain, llm_config=llm_config)


def get_llm_config() -> dict:
    return llm_settings.public_settings()


def save_llm_config(payload: dict) -> dict:
    return llm_settings.save_settings(payload)


def list_llm_models(payload: dict | None = None) -> dict:
    payload = payload or {}
    models = llm_settings.fetch_models(
        base_url=payload.get("base_url"),
        api_key=payload.get("api_key"),
    )
    return {"models": models}
