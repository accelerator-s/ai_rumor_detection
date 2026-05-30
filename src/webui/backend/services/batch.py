from __future__ import annotations

from src.core.batch import BatchInputError, run_batch_prediction
from src.webui.backend.errors import ServiceError
from src.webui.backend.state import state


def batch_predict(payload: dict) -> dict:
    if state.pipeline is None:
        raise ServiceError(state.error or "分类模型尚未加载，暂时无法进行检测。")
    if not isinstance(payload, dict):
        raise ServiceError("请求格式不正确，请刷新页面后重试。")
    try:
        return run_batch_prediction(state.pipeline.classifier, str(payload.get("content") or ""))
    except BatchInputError as exc:
        raise ServiceError(str(exc)) from exc
