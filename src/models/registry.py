from __future__ import annotations

from src.models.transformer import BertweetClassifier


def create_classifier(config: dict, checkpoint: str | None = None) -> BertweetClassifier:
    paths = config.get("paths", {})
    model_cfg = config.get("model", {})
    model_path = checkpoint or paths.get("checkpoint_dir") or paths.get("pretrained_model")
    return BertweetClassifier(
        model_path=model_path,
        model_name=model_cfg.get("name", "vinai/bertweet-base"),
        max_length=int(model_cfg.get("max_length", 128)),
    )

