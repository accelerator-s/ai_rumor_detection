from __future__ import annotations

import csv
import json
from pathlib import Path

from src.config import resolve_path
from src.data.dataset import read_examples
from src.evaluation.event_analysis import metrics_by_event
from src.evaluation.metrics import binary_metrics


def evaluate(classifier, csv_path: str | Path, output_dir: str | Path, config: dict | None = None) -> dict:
    examples = read_examples(csv_path, config=config)
    predictions = [classifier.predict(item.text, event=item.event) for item in examples]
    y_true = [int(item.label) for item in examples]
    y_pred = [item.label for item in predictions]

    result = {
        "overall": binary_metrics(y_true, y_pred),
        "by_event": metrics_by_event(examples, y_pred),
    }
    holdout_unique = _holdout_unique_metrics(examples, y_pred, config)
    if holdout_unique is not None:
        result["holdout_without_train_overlap"] = holdout_unique

    out_dir = resolve_path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metrics.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with (out_dir / "predictions.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text", "label", "prediction", "prob_0", "prob_1", "event"])
        for example, pred in zip(examples, predictions):
            writer.writerow([
                example.id,
                example.text,
                example.label,
                pred.label,
                pred.probabilities.get(0, 0.0),
                pred.probabilities.get(1, 0.0),
                example.event,
            ])
    return result


def _holdout_unique_metrics(examples, predictions: list[int], config: dict | None) -> dict | None:
    if not config:
        return None
    paths = config.get("paths", {})
    train_csv = paths.get("train_csv")
    if not train_csv:
        return None
    train_examples = read_examples(train_csv, config=config)
    train_texts = {item.text for item in train_examples if item.text}
    kept_examples = []
    kept_predictions = []
    overlap_count = 0
    for example, pred in zip(examples, predictions):
        if example.text in train_texts:
            overlap_count += 1
            continue
        kept_examples.append(example)
        kept_predictions.append(pred)
    if not kept_examples:
        return {
            "excluded_overlap_count": overlap_count,
            "evaluated_count": 0,
            "overall": binary_metrics([], []),
            "by_event": {},
        }
    return {
        "excluded_overlap_count": overlap_count,
        "evaluated_count": len(kept_examples),
        "overall": binary_metrics([int(item.label) for item in kept_examples], kept_predictions),
        "by_event": metrics_by_event(kept_examples, kept_predictions),
    }
