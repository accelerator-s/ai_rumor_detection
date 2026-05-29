from __future__ import annotations

from pathlib import Path

from src.config import resolve_path


def latest_checkpoint(checkpoint_dir: str | Path) -> Path | None:
    root = resolve_path(checkpoint_dir)
    if not root.exists():
        return None
    candidates = sorted(root.glob("best*"), key=lambda path: path.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def checkpoint_path(checkpoint_dir: str | Path, name: str = "best") -> Path:
    path = resolve_path(checkpoint_dir) / name
    path.mkdir(parents=True, exist_ok=True)
    return path

