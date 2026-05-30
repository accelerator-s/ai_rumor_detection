from __future__ import annotations

from src.webui.backend.services.llm import public_settings
from src.webui.backend.state import state


def health() -> dict:
    llm = public_settings()
    classifier_ready = state.pipeline is not None
    explanation_ready = classifier_ready and all(
        (
            llm.get("base_url"),
            llm.get("model"),
            llm.get("has_api_key"),
        )
    )
    return {
        "ok": explanation_ready,
        "error": state.error,
        "classifier_ready": classifier_ready,
        "explanation_ready": explanation_ready,
        "llm": llm,
    }
