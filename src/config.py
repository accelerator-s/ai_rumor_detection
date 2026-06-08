from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_config(path: str | Path = "configs/default.yaml") -> dict[str, Any]:
    config_path = resolve_path(path)
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def load_prompt_config(path: str | Path = "configs/prompt.yaml") -> dict[str, Any]:
    config_path = resolve_path(path)
    if not config_path.exists():
        return {}
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def resolve_path(path: str | Path) -> Path:
    path = Path(path)
    if path.is_absolute():
        return path
    return ROOT / path


def ensure_output_dirs(config: dict[str, Any]) -> None:
    paths = config.get("paths", {})
    value = paths.get("model_dir")
    if value:
        resolve_path(value).mkdir(parents=True, exist_ok=True)


def merge_dict(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_dict(result[key], value)
        else:
            result[key] = value
    return result

