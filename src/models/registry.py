from __future__ import annotations

from src.config import resolve_path
from src.models.transformer import BertweetClassifier
from src.training.checkpoint import is_trained_checkpoint, latest_checkpoint


def create_classifier(config: dict, checkpoint: str | None = None) -> BertweetClassifier:
    paths = config.get("paths", {})
    model_cfg = config.get("model", {})
    if checkpoint:
        model_path = resolve_path(checkpoint)
        if not is_trained_checkpoint(model_path):
            raise RuntimeError("指定的分类模型检查点不完整，请检查路径后重试。")
    else:
        model_path = latest_checkpoint(paths.get("checkpoint_dir", "outputs/checkpoints"))
        if model_path is None:
            raise RuntimeError("尚未找到训练后的分类模型。请先完成模型训练，再启动检测服务。")
    return BertweetClassifier(
        model_path=model_path,
        model_name=model_cfg.get("name", "vinai/bertweet-base"),
        max_length=int(model_cfg.get("max_length", 128)),
    )
