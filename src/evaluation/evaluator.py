from __future__ import annotations

import csv
import json
from pathlib import Path

from src.config import resolve_path
from src.data.dataset import read_examples
from src.evaluation.event_analysis import metrics_by_event
from src.evaluation.metrics import binary_metrics


def evaluate(classifier, csv_path: str | Path, output_dir: str | Path) -> dict:
    examples = read_examples(csv_path)
    predictions = [classifier.predict(item.text) for item in examples]
    y_true = [int(item.label) for item in examples]
    y_pred = [item.label for item in predictions]

    result = {
        "overall": binary_metrics(y_true, y_pred),
        "by_event": metrics_by_event(examples, y_pred),
    }

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

