from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from src.config import resolve_path
from src.data.preprocess import normalize_text


@dataclass(slots=True)
class RumorExample:
    id: str
    text: str
    label: int | None
    event: str


def read_examples(path: str | Path, with_label: bool = True) -> list[RumorExample]:
    csv_path = resolve_path(path)
    rows: list[RumorExample] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            label = int(row["label"]) if with_label and row.get("label") not in (None, "") else None
            rows.append(
                RumorExample(
                    id=str(row.get("id", "")),
                    text=normalize_text(row.get("text", "")),
                    label=label,
                    event=str(row.get("event", "")),
                )
            )
    return rows


def batches(items: list[RumorExample], batch_size: int) -> Iterable[list[RumorExample]]:
    for start in range(0, len(items), batch_size):
        yield items[start : start + batch_size]

