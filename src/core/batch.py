from __future__ import annotations

import csv
import io
import time

from src.data.preprocess import normalize_text
from src.evaluation.metrics import binary_metrics
from src.interfaces import Classifier

MAX_DETAIL_ROWS = 500


class BatchInputError(ValueError):
    pass


def run_batch_prediction(
    classifier: Classifier,
    content: str,
    max_detail_rows: int = MAX_DETAIL_ROWS,
) -> dict:
    if not str(content).strip():
        raise BatchInputError("请先选择需要评测的 CSV 文件。")

    reader = csv.DictReader(io.StringIO(str(content)))
    if reader.fieldnames is None or "text" not in reader.fieldnames:
        raise BatchInputError("CSV 文件缺少 text 列，请检查表头。")

    rows: list[dict] = []
    y_true: list[int] = []
    y_pred: list[int] = []
    label_dist = {0: 0, 1: 0}
    pred_dist = {0: 0, 1: 0}

    start = time.perf_counter()
    for index, raw in enumerate(reader):
        text = normalize_text(raw.get("text") or "")
        if not text:
            continue
        prediction = classifier.predict(text)
        pred = int(prediction.label)
        prob1 = float(prediction.probabilities.get(1, 0.0))
        pred_dist[pred] = pred_dist.get(pred, 0) + 1

        raw_label = raw.get("label")
        label: int | None = None
        if raw_label not in (None, ""):
            try:
                label = int(raw_label)
            except (TypeError, ValueError):
                label = None
        if label in (0, 1):
            label_dist[label] = label_dist.get(label, 0) + 1
            y_true.append(label)
            y_pred.append(pred)
        else:
            label = None

        row = {
            "id": str(raw.get("id", index)),
            "text": text,
            "pred": pred,
            "prob1": prob1,
        }
        if label is not None:
            row["label"] = label
            row["correct"] = label == pred
        rows.append(row)

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    if not rows:
        raise BatchInputError("CSV 文件中没有可用于评测的文本。")

    has_labels = bool(y_true)
    result: dict = {
        "count": len(rows),
        "elapsed_ms": round(elapsed_ms, 1),
        "has_labels": has_labels,
        "label_dist": label_dist,
        "pred_dist": pred_dist,
        "rows": rows[:max_detail_rows],
    }
    if has_labels:
        result["metrics"] = binary_metrics(y_true, y_pred)
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
        tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
        result["confusion"] = {"tp": tp, "fp": fp, "fn": fn, "tn": tn}
    return result
