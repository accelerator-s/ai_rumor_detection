from __future__ import annotations

from src.config import resolve_path
from src.models.transformer import BertweetClassifier
from src.training.checkpoint import is_trained_checkpoint


def create_classifier(config: dict, checkpoint: str | None = None) -> BertweetClassifier:
    from src.models.transformer import PerEventClassifier

    paths = config.get("paths", {})
    model_cfg = config.get("model", {})
    if checkpoint:
        model_path = resolve_path(checkpoint)
        if not is_trained_checkpoint(model_path):
            raise RuntimeError("指定的分类模型检查点不完整，请检查路径后重试。")
        return BertweetClassifier(
            model_path=model_path,
            model_name=model_cfg.get("name", "vinai/bertweet-base"),
            max_length=int(model_cfg.get("max_length", 128)),
        )
    model_root = resolve_path(paths.get("model_dir", "models/outputs"))
    event_dirs = sorted(model_root.glob("event_*"))
    if not event_dirs:
        raise RuntimeError("尚未找到训练后的分类模型。请先完成模型训练，再启动检测服务。")
    print(f"per-event models detected: {len(event_dirs)} events")
    return PerEventClassifier(model_root, model_cfg)  # type: ignore
