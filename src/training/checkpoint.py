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


def latest_checkpoint(checkpoint_dir: str | Path) -> Path | None:
    root = resolve_path(checkpoint_dir)
    if not root.exists():
        return None
    candidates = sorted(
        (path for path in root.glob("best*") if is_trained_checkpoint(path)),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def checkpoint_path(checkpoint_dir: str | Path, name: str = "best") -> Path:
    path = resolve_path(checkpoint_dir) / name
    path.mkdir(parents=True, exist_ok=True)
    return path
