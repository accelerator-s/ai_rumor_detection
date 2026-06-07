from __future__ import annotations

import csv
import io
import time

from src.core.events import EventInputError, normalize_event
from src.evaluation.metrics import binary_metrics
from src.interfaces import Classifier

MAX_DETAIL_ROWS = 500


class BatchInputError(ValueError):
    pass


def run_batch_prediction(
    classifier: Classifier,
    content: str,
    max_detail_rows: int = MAX_DETAIL_ROWS,
    config: dict | None = None,
) -> dict:
    if not str(content).strip():
        raise BatchInputError("请先选择需要评测的 CSV 文件。")

    # Validate CSV fields
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

    # Use temp file + read_examples for consistent cleaning with CLI
    import tempfile, os
    content_bytes = str(content).encode("utf-8")
    tmp = tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False)
    try:
        tmp.write(content_bytes)
        tmp.close()
        from src.data.dataset import read_examples
        examples = read_examples(tmp.name, with_label=True, config=config)
    finally:
        os.unlink(tmp.name)

    if not examples:
        raise BatchInputError("CSV 文件中没有可用于评测的文本。")

    rows: list[dict] = []
    y_true: list[int] = []
    y_pred: list[int] = []
    label_dist = {0: 0, 1: 0}
    pred_dist = {0: 0, 1: 0}

    start = time.perf_counter()
    for example in examples:
        try:
            event = normalize_event(example.event)
        except EventInputError as exc:
            raise BatchInputError(f"第 id={example.id} 行{str(exc)}") from exc
        prediction = classifier.predict(example.text, event=event)
        pred = int(prediction.label)
        prob1 = float(prediction.probabilities.get(1, 0.0))
        pred_dist[pred] = pred_dist.get(pred, 0) + 1

        label = int(example.label)
        label_dist[label] = label_dist.get(label, 0) + 1
        y_true.append(label)
        y_pred.append(pred)

        row = {
            "id": example.id,
            "text": example.text,
            "event": event,
            "pred": pred,
            "prob1": prob1,
            "label": label,
            "correct": label == pred,
        }
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
