from __future__ import annotations

import json
import math
import random
from collections import Counter
from pathlib import Path
from typing import Any

from src.config import resolve_path
from src.data.dataset import read_examples
from src.evaluation.event_analysis import metrics_by_event
from src.evaluation.metrics import binary_metrics
from src.training.checkpoint import checkpoint_path


def train(config: dict) -> Path:
    try:
        import joblib
        import torch
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import FeatureUnion, Pipeline
        from torch.utils.data import DataLoader
        from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup
    except ImportError as exc:
        raise RuntimeError("Install torch, transformers, scikit-learn, and joblib before training.") from exc

    seed = int(config.get("seed", 42))
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    paths = config["paths"]
    model_cfg = config["model"]
    train_cfg = config["training"]

    examples = read_examples(paths["train_csv"], config=config)
    if len(examples) < 2:
        raise RuntimeError("训练集样本不足，无法切分训练集和验证集。")

    stratify_labels = _split_stratify_labels(examples)
    valid_ratio = float(train_cfg.get("validation_ratio", 0.1))
    train_examples, valid_examples = train_test_split(
        examples,
        test_size=valid_ratio,
        random_state=seed,
        stratify=stratify_labels,
    )
    if not train_examples or not valid_examples:
        raise RuntimeError("训练集或内部验证集为空，请检查数据或切分配置。")

    print(f"training source: {paths['train_csv']} ({len(examples)} cleaned samples)")
    print(f"train split: {paths['train_csv']} ({len(train_examples)} samples, ratio={1 - valid_ratio:.2f})")
    print(f"internal valid split: {paths['train_csv']} ({len(valid_examples)} samples, ratio={valid_ratio:.2f})")
    print(f"holdout split excluded from training: {paths.get('val_csv', 'N/A')}")
    print(f"train label distribution: {_label_distribution(train_examples)}")
    print(f"valid label distribution: {_label_distribution(valid_examples)}")

    tfidf_model = _train_tfidf_model(train_examples, train_cfg, TfidfVectorizer, LogisticRegression, FeatureUnion, Pipeline)

    tokenizer = AutoTokenizer.from_pretrained(resolve_path(paths["pretrained_model"]), use_fast=False)
    event_to_id = _event_to_id(examples)
    pretrained_path = resolve_path(paths["pretrained_model"])
    hf_config = AutoConfig.from_pretrained(
        pretrained_path,
        num_labels=int(model_cfg.get("num_labels", 2)),
    )
    if "hidden_dropout_prob" in train_cfg:
        hf_config.hidden_dropout_prob = float(train_cfg["hidden_dropout_prob"])
    if "attention_dropout_prob" in train_cfg:
        hf_config.attention_probs_dropout_prob = float(train_cfg["attention_dropout_prob"])
    if "classifier_dropout" in train_cfg:
        hf_config.classifier_dropout = float(train_cfg["classifier_dropout"])

    model = AutoModelForSequenceClassification.from_pretrained(pretrained_path, config=hf_config)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    def collate(batch):
        texts = [_model_text(item) for item in batch]
        labels = torch.tensor([item.label for item in batch], dtype=torch.long)
        encoded = tokenizer(
            texts,
            truncation=True,
            max_length=int(model_cfg.get("max_length", 128)),
            padding=True,
            return_tensors="pt",
        )
        encoded["labels"] = labels
        encoded["event_labels"] = torch.tensor([event_to_id[str(item.event).strip()] for item in batch], dtype=torch.long)
        return encoded

    loader = DataLoader(
        train_examples,
        batch_size=int(train_cfg.get("batch_size", 8)),
        shuffle=True,
        collate_fn=collate,
    )

    class_weights = _class_weights(train_examples, int(model_cfg.get("num_labels", 2)), train_cfg)
    weight_tensor = torch.tensor(class_weights, dtype=torch.float, device=device) if class_weights else None
    loss_fn = torch.nn.CrossEntropyLoss(
        weight=weight_tensor,
        label_smoothing=float(train_cfg.get("label_smoothing", 0.0)),
    )

    event_loss_fn = torch.nn.CrossEntropyLoss()
    event_loss_weight = float(train_cfg.get("event_loss_weight", 0.0))
    event_head = torch.nn.Linear(int(hf_config.hidden_size), len(event_to_id)).to(device) if event_loss_weight > 0 else None

    optimizer_groups = _optimizer_groups(model, train_cfg)
    if event_head is not None:
        optimizer_groups.append(
            {
                "params": list(event_head.parameters()),
                "lr": float(train_cfg.get("head_learning_rate", train_cfg.get("learning_rate", 2e-5))),
                "weight_decay": float(train_cfg.get("weight_decay", 0.01)),
            }
        )

    optimizer = torch.optim.AdamW(
        optimizer_groups,
        lr=float(train_cfg.get("learning_rate", 2e-5)),
        weight_decay=float(train_cfg.get("weight_decay", 0.01)),
    )

    accumulation_steps = max(1, int(train_cfg.get("gradient_accumulation_steps", 1)))
    epochs = int(train_cfg.get("epochs", 3))
    total_optimizer_steps = max(1, math.ceil(len(loader) / accumulation_steps) * epochs)
    warmup_steps = int(total_optimizer_steps * float(train_cfg.get("warmup_ratio", 0.0)))
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_optimizer_steps,
    )

    use_mixed_precision = bool(train_cfg.get("mixed_precision", True)) and device.type == "cuda"
    scaler = torch.cuda.amp.GradScaler(enabled=use_mixed_precision)
    early_stopping_patience = max(1, int(train_cfg.get("early_stopping_patience", 2)))
    max_grad_norm = float(train_cfg.get("max_grad_norm", 1.0))

    best_score = (-1.0, -1.0, -1.0)
    best_metrics: dict[str, Any] = {}
    best_epoch = 0
    best_ensemble_weight = 0.5
    patience = 0
    early_stopped = False
    best_dir = checkpoint_path(paths["checkpoint_dir"], "best")
    metrics_dir = resolve_path(paths.get("metrics_dir", "outputs/metrics"))
    metrics_dir.mkdir(parents=True, exist_ok=True)
    history_path = metrics_dir / "train_history.json"
    history: list[dict] = []

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        running_loss = 0.0
        optimizer_steps = 0

        for step, batch in enumerate(loader, start=1):
            labels = batch.pop("labels").to(device)
            event_labels = batch.pop("event_labels").to(device)
            batch = {key: value.to(device) for key, value in batch.items()}
            with torch.cuda.amp.autocast(enabled=use_mixed_precision):
                outputs = model(**batch, output_hidden_states=event_head is not None)
                logits = outputs.logits
                loss = loss_fn(logits, labels)
                if event_head is not None:
                    pooled = outputs.hidden_states[-1][:, 0]
                    event_loss = event_loss_fn(event_head(pooled), event_labels)
                    loss = loss + event_loss_weight * event_loss
                scaled_loss = loss / accumulation_steps

            scaler.scale(scaled_loss).backward()
            running_loss += float(loss.item())

            should_step = step % accumulation_steps == 0 or step == len(loader)
            if should_step:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()
                scheduler.step()
                optimizer_steps += 1

        metrics = _evaluate_model(
            model,
            tokenizer,
            tfidf_model,
            valid_examples,
            model_cfg,
            train_cfg,
            device,
            torch,
            loss_fn,
        )
        avg_loss = running_loss / max(1, len(loader))
        score = _selection_score(metrics, train_cfg)
        epoch_record = {
            "epoch": epoch + 1,
            "train_loss": round(avg_loss, 6),
            "valid_loss": round(metrics["loss"], 6),
            "optimizer_steps": optimizer_steps,
            "learning_rates": [round(group["lr"], 10) for group in optimizer.param_groups],
            "threshold": metrics["threshold"],
            "ensemble_weight": metrics["ensemble_weight"],
            "accuracy": round(metrics["accuracy"], 6),
            "precision": round(metrics["precision"], 6),
            "recall": round(metrics["recall"], 6),
            "f1": round(metrics["f1"], 6),
            "confusion_matrix": metrics["confusion_matrix"],
            "label_distribution": metrics["label_distribution"],
            "by_event": metrics["by_event"],
            "class_weights": class_weights,
            "split": {
                "source": paths["train_csv"],
                "validation_ratio": valid_ratio,
                "train_samples": len(train_examples),
                "valid_samples": len(valid_examples),
                "holdout_excluded": paths.get("val_csv"),
            },
        }
        history.append(epoch_record)
        history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")

        print(
            f"epoch {epoch + 1}/{epochs} | "
            f"train_loss={avg_loss:.4f} | "
            f"valid_loss={metrics['loss']:.4f} | "
            f"val_acc={metrics['accuracy']:.4f} | "
            f"val_precision={metrics['precision']:.4f} | "
            f"val_recall={metrics['recall']:.4f} | "
            f"val_f1={metrics['f1']:.4f} | "
            f"threshold={metrics['threshold']:.2f} | "
            f"bert_weight={metrics['ensemble_weight']:.2f} | "
            f"pred_dist={metrics['prediction_distribution']} | "
            f"optimizer_steps={optimizer_steps}"
        )

        if score > best_score:
            best_score = score
            best_metrics = metrics
            best_epoch = epoch + 1
            best_ensemble_weight = float(metrics["ensemble_weight"])
            patience = 0
            model.save_pretrained(best_dir)
            tokenizer.save_pretrained(best_dir)
            joblib.dump(tfidf_model, best_dir / "tfidf_model.joblib")
            _write_training_metadata(
                best_dir,
                best_epoch,
                best_metrics,
                class_weights,
                config,
                train_examples,
                valid_examples,
                valid_ratio,
            )
        else:
            patience += 1
            if patience >= early_stopping_patience:
                early_stopped = True
                print(f"early stopping triggered after epoch {epoch + 1}")
                break

    print(
        f"training finished | best_epoch={best_epoch} | "
        f"best_val_f1={best_metrics.get('f1', 0.0):.4f} | "
        f"best_threshold={best_metrics.get('threshold', 0.5):.2f} | "
        f"best_bert_weight={best_ensemble_weight:.2f} | "
        f"early_stopped={early_stopped} | history_file={history_path}"
    )
    return best_dir


def _event_to_id(examples) -> dict[str, int]:
    return {event: index for index, event in enumerate(sorted({str(item.event).strip() for item in examples if str(item.event).strip()}))}


def _model_text(item) -> str:
    return item.text


def _tfidf_text(item) -> str:
    return f"__event_{item.event}__ {item.text}"


def _train_tfidf_model(train_examples, train_cfg: dict, vectorizer_cls, logreg_cls, feature_union_cls, pipeline_cls):
    texts = [_tfidf_text(item) for item in train_examples]
    labels = [int(item.label) for item in train_examples]
    model = pipeline_cls(
        [
            (
                "features",
                feature_union_cls(
                    [
                        (
                            "word",
                            vectorizer_cls(
                                analyzer="word",
                                ngram_range=tuple(train_cfg.get("tfidf_word_ngram_range", (1, 2))),
                                min_df=int(train_cfg.get("tfidf_word_min_df", 2)),
                                max_df=float(train_cfg.get("tfidf_word_max_df", 0.95)),
                                sublinear_tf=True,
                            ),
                        ),
                        (
                            "char",
                            vectorizer_cls(
                                analyzer="char_wb",
                                ngram_range=tuple(train_cfg.get("tfidf_char_ngram_range", (3, 5))),
                                min_df=int(train_cfg.get("tfidf_char_min_df", 2)),
                                max_df=float(train_cfg.get("tfidf_char_max_df", 1.0)),
                                sublinear_tf=True,
                            ),
                        ),
                    ]
                ),
            ),
            (
                "classifier",
                logreg_cls(
                    C=float(train_cfg.get("tfidf_logreg_c", 2.0)),
                    class_weight=train_cfg.get("tfidf_class_weight", None),
                    max_iter=int(train_cfg.get("tfidf_max_iter", 3000)),
                    solver="lbfgs",
                    random_state=int(train_cfg.get("tfidf_seed", 42)),
                ),
            ),
        ]
    )
    model.fit(texts, labels)
    return model

def _class_weights(examples, num_labels: int, train_cfg: dict) -> list[float] | None:
    if train_cfg.get("class_weighting", "balanced") == "none":
        return None
    counts = Counter(int(item.label) for item in examples if item.label is not None)
    total = sum(counts.values())
    if total == 0:
        return None
    return [total / (num_labels * max(1, counts.get(label, 0))) for label in range(num_labels)]


def _optimizer_groups(model, train_cfg: dict) -> list[dict]:
    base_lr = float(train_cfg.get("learning_rate", 2e-5))
    head_lr = float(train_cfg.get("head_learning_rate", base_lr))
    weight_decay = float(train_cfg.get("weight_decay", 0.01))
    layerwise_decay = float(train_cfg.get("layerwise_lr_decay", 1.0))
    no_decay = ("bias", "LayerNorm.weight", "layer_norm.weight")

    groups: dict[tuple[float, float], dict] = {}
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        lr = _parameter_lr(name, base_lr, head_lr, layerwise_decay)
        decay = 0.0 if any(item in name for item in no_decay) else weight_decay
        key = (lr, decay)
        groups.setdefault(key, {"params": [], "lr": lr, "weight_decay": decay})["params"].append(param)
    return list(groups.values())


def _parameter_lr(name: str, base_lr: float, head_lr: float, layerwise_decay: float) -> float:
    if "classifier" in name or "score" in name:
        return head_lr
    layer_idx = _extract_layer_index(name)
    if layer_idx is None or layerwise_decay >= 1.0:
        return base_lr
    return base_lr * (layerwise_decay ** max(0, 11 - layer_idx))


def _extract_layer_index(name: str) -> int | None:
    parts = name.split(".")
    for marker in ("layer", "layers"):
        if marker in parts:
            idx = parts.index(marker) + 1
            if idx < len(parts) and parts[idx].isdigit():
                return int(parts[idx])
    return None


def _evaluate_model(model, tokenizer, tfidf_model, examples, model_cfg, train_cfg, device, torch, loss_fn) -> dict[str, Any]:
    y_true: list[int] = []
    bert_probabilities: list[float] = []
    losses: list[float] = []
    model.eval()
    for item in examples:
        encoded = tokenizer(
            _model_text(item),
            truncation=True,
            max_length=int(model_cfg.get("max_length", 128)),
            padding=True,
            return_tensors="pt",
        )
        encoded = {key: value.to(device) for key, value in encoded.items()}
        label = torch.tensor([int(item.label)], dtype=torch.long, device=device)
        with torch.no_grad():
            logits = model(**encoded).logits
            losses.append(float(loss_fn(logits, label).item()))
            prob_1 = torch.softmax(logits, dim=-1)[0, 1].detach().cpu().item()
        y_true.append(int(item.label))
        bert_probabilities.append(float(prob_1))

    tfidf_probabilities = [float(item) for item in tfidf_model.predict_proba([_tfidf_text(item) for item in examples])[:, 1]]
    ensemble_metrics = _best_ensemble_metrics(y_true, bert_probabilities, tfidf_probabilities, train_cfg)
    threshold = ensemble_metrics["threshold"]
    probabilities = ensemble_metrics["probabilities"]
    y_pred = [int(prob >= threshold) for prob in probabilities]
    metrics = binary_metrics(y_true, y_pred)
    metrics.update({key: value for key, value in ensemble_metrics.items() if key != "probabilities"})
    metrics["loss"] = sum(losses) / max(1, len(losses))
    metrics["label_distribution"] = dict(sorted(Counter(y_true).items()))
    metrics["prediction_distribution"] = dict(sorted(Counter(y_pred).items()))
    metrics["confusion_matrix"] = _confusion_matrix(y_true, y_pred)
    metrics["by_event"] = metrics_by_event(examples, y_pred)
    return metrics


def _best_ensemble_metrics(
    y_true: list[int],
    bert_probabilities: list[float],
    tfidf_probabilities: list[float],
    train_cfg: dict,
) -> dict[str, Any]:
    min_weight = float(train_cfg.get("ensemble_bert_weight_min", 0.3))
    max_weight = float(train_cfg.get("ensemble_bert_weight_max", 0.7))
    step = float(train_cfg.get("ensemble_bert_weight_step", 0.1))
    steps = max(1, int(round((max_weight - min_weight) / step)))

    best: dict[str, Any] = {}
    best_score = (-1.0, -1.0, -1.0)
    for idx in range(steps + 1):
        weight = round(min_weight + idx * step, 6)
        probabilities = [
            weight * bert_prob + (1.0 - weight) * tfidf_prob
            for bert_prob, tfidf_prob in zip(bert_probabilities, tfidf_probabilities)
        ]
        threshold_metrics = _best_threshold_metrics(y_true, probabilities, train_cfg)
        score = _selection_score(threshold_metrics["threshold_metrics"], train_cfg)
        if score > best_score:
            best_score = score
            best = {
                "ensemble_weight": weight,
                "threshold": threshold_metrics["threshold"],
                "threshold_metrics": threshold_metrics["threshold_metrics"],
                "probabilities": probabilities,
            }
    return best


def _best_threshold_metrics(y_true: list[int], probabilities: list[float], train_cfg: dict) -> dict[str, Any]:
    threshold_min = float(train_cfg.get("threshold_min", 0.3))
    threshold_max = float(train_cfg.get("threshold_max", 0.7))
    threshold_step = float(train_cfg.get("threshold_step", 0.01))
    steps = max(1, int(round((threshold_max - threshold_min) / threshold_step)))

    best_threshold = 0.5
    best_metrics: dict[str, float] = {}
    best_score = (-1.0, -1.0, -1.0)
    for idx in range(steps + 1):
        threshold = round(threshold_min + idx * threshold_step, 6)
        y_pred = [int(prob >= threshold) for prob in probabilities]
        metrics = binary_metrics(y_true, y_pred)
        score = (metrics["f1"], metrics["accuracy"], min(metrics["precision"], metrics["recall"]))
        if score > best_score:
            best_score = score
            best_threshold = threshold
            best_metrics = metrics
    return {"threshold": best_threshold, "threshold_metrics": best_metrics}


def _selection_score(metrics: dict[str, Any], train_cfg: dict | None = None) -> tuple[float, float, float]:
    selection_metric = (train_cfg or {}).get("selection_metric", "accuracy")
    if selection_metric == "f1":
        return (float(metrics["f1"]), float(metrics["accuracy"]), min(float(metrics["precision"]), float(metrics["recall"])))
    return (float(metrics["accuracy"]), float(metrics["f1"]), min(float(metrics["precision"]), float(metrics["recall"])))


def _confusion_matrix(y_true: list[int], y_pred: list[int]) -> dict[str, int]:
    return {
        "tp": sum(int(a == 1 and b == 1) for a, b in zip(y_true, y_pred)),
        "tn": sum(int(a == 0 and b == 0) for a, b in zip(y_true, y_pred)),
        "fp": sum(int(a == 0 and b == 1) for a, b in zip(y_true, y_pred)),
        "fn": sum(int(a == 1 and b == 0) for a, b in zip(y_true, y_pred)),
    }


def _write_training_metadata(
    best_dir: Path,
    best_epoch: int,
    metrics: dict[str, Any],
    class_weights: list[float] | None,
    config: dict,
    train_examples,
    valid_examples,
    valid_ratio: float,
) -> None:
    metadata = {
        "best_epoch": best_epoch,
        "best_threshold": metrics["threshold"],
        "ensemble_bert_weight": metrics["ensemble_weight"],
        "tokenizer_path": str(resolve_path(config["paths"].get("pretrained_model", "models/pretrained"))),
        "internal_validation_metrics": {
            "loss": metrics["loss"],
            "accuracy": metrics["accuracy"],
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1": metrics["f1"],
            "ensemble_weight": metrics["ensemble_weight"],
            "confusion_matrix": metrics["confusion_matrix"],
            "label_distribution": metrics["label_distribution"],
            "prediction_distribution": metrics["prediction_distribution"],
            "by_event": metrics["by_event"],
        },
        "class_weights": class_weights,
        "training": config.get("training", {}),
        "split": {
            "source": config["paths"]["train_csv"],
            "validation_ratio": valid_ratio,
            "train_samples": len(train_examples),
            "valid_samples": len(valid_examples),
            "holdout_excluded": config["paths"].get("val_csv"),
        },
    }
    (best_dir / "training_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _split_stratify_labels(examples) -> list[str]:
    groups = [f"{item.event}:{int(item.label)}" for item in examples]
    counts = Counter(groups)
    if min(counts.values()) < 2:
        return [str(int(item.label)) for item in examples]
    return groups


def _label_distribution(examples) -> dict[int, int]:
    return dict(sorted(Counter(int(item.label) for item in examples if item.label is not None).items()))
