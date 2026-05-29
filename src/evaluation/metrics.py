from __future__ import annotations


def binary_metrics(y_true: list[int], y_pred: list[int], positive: int = 1) -> dict[str, float]:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    total = len(y_true)
    if total == 0:
        return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}

    correct = sum(int(a == b) for a, b in zip(y_true, y_pred))
    tp = sum(int(a == positive and b == positive) for a, b in zip(y_true, y_pred))
    fp = sum(int(a != positive and b == positive) for a, b in zip(y_true, y_pred))
    fn = sum(int(a == positive and b != positive) for a, b in zip(y_true, y_pred))

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "accuracy": correct / total,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }

