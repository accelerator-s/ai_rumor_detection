from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from src.config import resolve_path
from src.data.preprocess import URL_RE, normalize_text


@dataclass(slots=True)
class RumorExample:
    id: str
    text: str
    label: int | None
    event: str


@dataclass(slots=True)
class CleaningStats:
    source: str
    original_count: int
    cleaned_count: int
    duplicate_count: int
    empty_count: int
    conflict_count: int


def _cleaning_config(config: dict | None) -> dict:
    return (config or {}).get("data_cleaning", {})


def _normalize_example_text(text: str, config: dict | None = None) -> str:
    cleaning = _cleaning_config(config)
    return normalize_text(text, emoji_normalization=bool(cleaning.get("emoji_normalization", True)))


def _body_without_urls(text: str, config: dict | None = None) -> str:
    normalized = _normalize_example_text(text, config=config)
    return " ".join(URL_RE.sub(" ", normalized.replace("HTTPURL", " ").replace("IMAGEURL", " ")).split())


def read_examples(
    path: str | Path,
    with_label: bool = True,
    config: dict | None = None,
) -> list[RumorExample]:
    rows = _read_raw_examples(path, with_label=with_label)
    if not _cleaning_config(config).get("enabled", True):
        return rows
    cleaned, _stats, _conflicts = clean_examples(rows, source=str(path), config=config)
    return cleaned


def clean_examples(
    examples: list[RumorExample],
    source: str,
    config: dict | None = None,
) -> tuple[list[RumorExample], CleaningStats, list[dict]]:
    raw_conflict_ids, conflicts = _raw_text_label_conflicts(examples, source)
    empty_count = 0
    duplicate_count = 0
    candidates: list[tuple[RumorExample, str]] = []
    seen_raw_texts: set[str] = set()

    for example in examples:
        if example.id in raw_conflict_ids:
            continue
        if example.text in seen_raw_texts:
            duplicate_count += 1
            continue
        seen_raw_texts.add(example.text)
        text = _normalize_example_text(example.text, config=config)
        if not text:
            empty_count += 1
            continue
        candidates.append((RumorExample(id=example.id, text=text, label=example.label, event=example.event), example.text))

    body_groups: dict[str, list[tuple[RumorExample, str]]] = defaultdict(list)
    for normalized, raw_text in candidates:
        body_groups[_body_without_urls(raw_text, config=config)].append((normalized, raw_text))

    cleaned: list[RumorExample] = []
    for group in body_groups.values():
        labels = {item.label for item, _raw_text in group if item.label is not None}
        raw_texts = {raw_text for _item, raw_text in group}
        if len(labels) == 1 and len(raw_texts) > 1:
            cleaned.append(group[0][0])
            duplicate_count += len(group) - 1
            continue
        cleaned.extend(item for item, _raw_text in group)

    stats = CleaningStats(
        source=source,
        original_count=len(examples),
        cleaned_count=len(cleaned),
        duplicate_count=duplicate_count,
        empty_count=empty_count,
        conflict_count=len(conflicts),
    )
    return cleaned, stats, conflicts


def _raw_text_label_conflicts(examples: list[RumorExample], source: str) -> tuple[set[str], list[dict]]:
    groups: dict[str, list[RumorExample]] = defaultdict(list)
    for example in examples:
        if example.label is not None:
            groups[example.text].append(example)

    conflict_ids: set[str] = set()
    conflicts: list[dict] = []
    for raw_text, group in groups.items():
        labels = sorted({int(item.label) for item in group if item.label is not None})
        if len(labels) <= 1:
            continue
        example_ids = [item.id for item in group]
        conflict_ids.update(example_ids)
        conflicts.append(
            {
                "type": "raw_text_label_conflict",
                "text": raw_text,
                "labels": labels,
                "example_ids": example_ids,
                "source": source,
                "action": "removed_all",
            }
        )
    return conflict_ids, conflicts


def overlap_stats(left: Iterable[RumorExample], right: Iterable[RumorExample]) -> dict:
    left_by_text = {item.text: item.id for item in left if item.text}
    right_by_text = {item.text: item.id for item in right if item.text}
    overlap_texts = sorted(set(left_by_text) & set(right_by_text))
    return {
        "overlap_count": len(overlap_texts),
        "samples": [
            {
                "text": text,
                "left_id": left_by_text[text],
                "right_id": right_by_text[text],
            }
            for text in overlap_texts[:20]
        ],
    }


def _read_raw_examples(path: str | Path, with_label: bool = True) -> list[RumorExample]:
    csv_path = resolve_path(path)
    rows: list[RumorExample] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            label = int(row["label"]) if with_label and row.get("label") not in (None, "") else None
            rows.append(
                RumorExample(
                    id=str(row.get("id", "")),
                    text=str(row.get("text", "")),
                    label=label,
                    event=str(row.get("event", "")),
                )
            )
    return rows


def batches(items: list[RumorExample], batch_size: int) -> Iterable[list[RumorExample]]:
    for start in range(0, len(items), batch_size):
        yield items[start : start + batch_size]
