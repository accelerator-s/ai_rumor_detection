from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
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


def read_examples(
    path: str | Path,
    with_label: bool = True,
    config: dict | None = None,
) -> list[RumorExample]:
    rows = _read_raw_examples(path, with_label=with_label)
    if not _cleaning_config(config).get("enabled", True):
        return [
            RumorExample(
                id=item.id,
                text=_normalize_example_text(item.text, config=config),
                label=item.label,
                event=item.event,
            )
            for item in rows
        ]
    cleaned, _stats, _conflicts = clean_examples(rows, source=str(path), config=config)
    return cleaned


def clean_examples(
    examples: list[RumorExample],
    source: str,
    config: dict | None = None,
) -> tuple[list[RumorExample], CleaningStats, list[dict]]:
    cleaning = _cleaning_config(config)
    deduplicate = bool(cleaning.get("deduplicate", True))

    cleaned: list[RumorExample] = []
    duplicate_count = 0
    empty_count = 0
    conflicts: list[dict] = []
    seen_labels: dict[str, set[int]] = defaultdict(set)
    seen_example: dict[str, RumorExample] = {}

    for example in examples:
        text = _normalize_example_text(example.text, config=config)
        if not text:
            empty_count += 1
            continue
        normalized = RumorExample(id=example.id, text=text, label=example.label, event=example.event)
        if normalized.label is not None:
            seen_labels[normalized.text].add(int(normalized.label))
            if len(seen_labels[normalized.text]) > 1:
                conflicts.append(
                    {
                        "text": normalized.text,
                        "labels": sorted(seen_labels[normalized.text]),
                        "example_ids": [seen_example[normalized.text].id, normalized.id]
                        if normalized.text in seen_example
                        else [normalized.id],
                        "source": source,
                    }
                )
        if deduplicate and normalized.text in seen_example:
            duplicate_count += 1
            continue
        seen_example[normalized.text] = normalized
        cleaned.append(normalized)

    conflict_items = _deduplicate_conflicts(conflicts)
    stats = CleaningStats(
        source=source,
        original_count=len(examples),
        cleaned_count=len(cleaned),
        duplicate_count=duplicate_count,
        empty_count=empty_count,
        conflict_count=len(conflict_items),
    )
    return cleaned, stats, conflict_items


def _deduplicate_conflicts(conflicts: list[dict]) -> list[dict]:
    merged: dict[str, dict] = {}
    for item in conflicts:
        key = item["text"]
        if key not in merged:
            merged[key] = item
            continue
        merged[key]["labels"] = sorted(set(merged[key]["labels"]) | set(item["labels"]))
        merged[key]["example_ids"] = sorted(set(merged[key]["example_ids"]) | set(item["example_ids"]))
    return list(merged.values())


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


def export_cleaned_datasets(config: dict) -> dict:
    paths = config.get("paths", {})
    train_path = paths.get("train_csv")
    val_path = paths.get("val_csv")
    if not train_path or not val_path:
        raise RuntimeError("配置中缺少 train_csv 或 val_csv，无法导出清洗结果。")

    raw_train = _read_raw_examples(train_path)
    raw_val = _read_raw_examples(val_path)
    cleaned_train, train_stats, train_conflicts = clean_examples(raw_train, source=str(train_path), config=config)
    cleaned_val, val_stats, val_conflicts = clean_examples(raw_val, source=str(val_path), config=config)
    overlap = overlap_stats(cleaned_train, cleaned_val)

    cleaned_train_path = resolve_path(paths.get("cleaned_train_csv", "outputs/cleaned/train.cleaned.csv"))
    cleaned_val_path = resolve_path(paths.get("cleaned_val_csv", "outputs/cleaned/val.cleaned.csv"))
    report_path = resolve_path(paths.get("cleaning_report_json", "outputs/cleaned/cleaning_report.json"))
    cleaned_train_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_val_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    _write_examples_csv(cleaned_train_path, cleaned_train)
    _write_examples_csv(cleaned_val_path, cleaned_val)

    report = {
        "train": asdict(train_stats),
        "val": asdict(val_stats),
        "train_conflicts": train_conflicts,
        "val_conflicts": val_conflicts,
        "train_val_overlap": overlap,
        "output_files": {
            "cleaned_train_csv": str(cleaned_train_path),
            "cleaned_val_csv": str(cleaned_val_path),
            "cleaning_report_json": str(report_path),
        },
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


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


def _write_examples_csv(path: Path, examples: list[RumorExample]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text", "label", "event"])
        for item in examples:
            writer.writerow([item.id, item.text, item.label, item.event])


def batches(items: list[RumorExample], batch_size: int) -> Iterable[list[RumorExample]]:
    for start in range(0, len(items), batch_size):
        yield items[start : start + batch_size]
