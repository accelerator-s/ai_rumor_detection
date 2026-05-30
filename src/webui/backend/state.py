from __future__ import annotations

from src.pipeline import build_pipeline


class AppState:
    def __init__(self) -> None:
        self.pipeline = None
        self.error: str | None = None

    def load(self, config_path: str = "configs/default.yaml", with_explainer: bool = True) -> None:
        try:
            self.pipeline = build_pipeline(config_path, with_explainer=with_explainer)
            self.error = None
        except Exception as exc:
            self.pipeline = None
            self.error = str(exc).strip() or "服务初始化失败。请检查模型文件、运行环境和配置后重试。"


state = AppState()
