from __future__ import annotations

import csv
import io
import time

from src.core.events import EventInputError, normalize_event
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
    required_fields = {"id", "text", "label", "event"}
    fieldnames = set(reader.fieldnames or [])
    if fieldnames != required_fields:
        missing = sorted(required_fields - fieldnames)
        extra = sorted(fieldnames - required_fields)
        details = []
        if missing:
            details.append(f"缺少列: {', '.join(missing)}")
        if extra:
            details.append(f"不支持的列: {', '.join(extra)}")
        raise BatchInputError(f"CSV 文件字段不符合标准，{'；'.join(details)}。")

    rows: list[dict] = []
    y_true: list[int] = []
    y_pred: list[int] = []
    label_dist = {0: 0, 1: 0}
    pred_dist = {0: 0, 1: 0}

    start = time.perf_counter()
    for index, raw in enumerate(reader):
        raw_id = str(raw.get("id") or "").strip()
        try:
            event = normalize_event(raw.get("event"))
        except EventInputError as exc:
            raise BatchInputError(f"第 {index + 2} 行{str(exc)}") from exc
        if not raw_id:
            raise BatchInputError(f"第 {index + 2} 行缺少 id。")
        text = normalize_text(raw.get("text") or "", emoji_normalization=True)
        if not text:
            raise BatchInputError(f"第 {index + 2} 行缺少 text。")
        prediction = classifier.predict(text, event=event)
        pred = int(prediction.label)
        prob1 = float(prediction.probabilities.get(1, 0.0))
        pred_dist[pred] = pred_dist.get(pred, 0) + 1

        raw_label = str(raw.get("label") or "").strip()
        if raw_label == "":
            raise BatchInputError(f"第 {index + 2} 行缺少 label。")
        try:
            label = int(raw_label)
        except (TypeError, ValueError) as exc:
            raise BatchInputError(f"第 {index + 2} 行 label 必须是 0 或 1。") from exc
        if label not in (0, 1):
            raise BatchInputError(f"第 {index + 2} 行 label 必须是 0 或 1。")
        label_dist[label] = label_dist.get(label, 0) + 1
        y_true.append(label)
        y_pred.append(pred)

        row = {
            "id": raw_id,
            "text": text,
            "event": event,
            "pred": pred,
            "prob1": prob1,
        }
        row["label"] = label
        row["correct"] = label == pred
        rows.append(row)

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    if not rows:
        raise BatchInputError("CSV 文件中没有可用于评测的文本。")

    result: dict = {
        "count": len(rows),
        "elapsed_ms": round(elapsed_ms, 1),
        "has_labels": True,
        "label_dist": label_dist,
        "pred_dist": pred_dist,
        "rows": rows[:max_detail_rows],
        "metrics": binary_metrics(y_true, y_pred),
    }
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    result["confusion"] = {"tp": tp, "fp": fp, "fn": fn, "tn": tn}
    return result
