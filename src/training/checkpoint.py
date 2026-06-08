from __future__ import annotations

from pathlib import Path

from src.config import resolve_path


def is_trained_checkpoint(path: str | Path) -> bool:
    target = resolve_path(path)
    weight_files = ("model.safetensors", "pytorch_model.bin")
    return (
        target.is_dir()
        and (target / "config.json").is_file()
        and any((target / name).is_file() for name in weight_files)
    )


def checkpoint_path(model_dir: str | Path, name: str) -> Path:
    path = resolve_path(model_dir) / name
    path.mkdir(parents=True, exist_ok=True)
    return path
