from __future__ import annotations

from src.webui.backend.errors import ServiceError
from src.webui.backend.services.llm import require_settings
from src.webui.backend.state import state


def predict(text: str, explain: bool = True) -> dict:
    if not text.strip():
        raise ServiceError("请输入需要检测的文本。")
    if state.pipeline is None:
        raise ServiceError(state.error or "分类模型尚未加载，暂时无法进行检测。")
    llm_config = require_settings() if explain else None
    return state.pipeline.predict(text, explain=explain, llm_config=llm_config)
