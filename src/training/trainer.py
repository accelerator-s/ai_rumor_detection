from __future__ import annotations

import json
import math
import random
from collections import Counter
from pathlib import Path

from src.config import resolve_path
from src.data.dataset import read_examples
from src.evaluation.metrics import binary_metrics
from src.training.checkpoint import checkpoint_path


def train(config: dict) -> Path:
    try:
        import torch
        from sklearn.model_selection import train_test_split
        from torch.utils.data import DataLoader
        from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup
    except ImportError as exc:
        raise RuntimeError("Install torch, transformers, and scikit-learn before training.") from exc

    seed = int(config.get("seed", 42))
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    paths = config["paths"]
    model_cfg = config["model"]
    train_cfg = config["training"]

    examples = read_examples(paths["train_csv"])
    if len(examples) < 2:
        raise RuntimeError("训练集样本不足，无法切分训练集和验证集。")

    labels = [int(item.label) for item in examples]
    valid_ratio = float(train_cfg.get("validation_ratio", 0.1))
    train_examples, valid_examples = train_test_split(
        examples,
        test_size=valid_ratio,
        random_state=seed,
        stratify=labels,
    )
    if not train_examples or not valid_examples:
        raise RuntimeError("训练集或内部验证集为空，请检查数据或切分配置。")

    print(f"train split: {paths['train_csv']} ({len(train_examples)} samples)")
    print(f"internal valid split: {paths['train_csv']} ({len(valid_examples)} samples, ratio={valid_ratio:.2f})")
    print(f"train label distribution: {_label_distribution(train_examples)}")
    print(f"valid label distribution: {_label_distribution(valid_examples)}")

    tokenizer = AutoTokenizer.from_pretrained(resolve_path(paths["pretrained_model"]), use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(
        resolve_path(paths["pretrained_model"]),
        num_labels=int(model_cfg.get("num_labels", 2)),
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    def collate(batch):
        texts = [item.text for item in batch]
        labels = torch.tensor([item.label for item in batch], dtype=torch.long)
        encoded = tokenizer(
            texts,
            truncation=True,
            max_length=int(model_cfg.get("max_length", 128)),
            padding=True,
            return_tensors="pt",
        )
        encoded["labels"] = labels
        return encoded

    loader = DataLoader(
        train_examples,
        batch_size=int(train_cfg.get("batch_size", 8)),
        shuffle=True,
        collate_fn=collate,
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
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

    best_f1 = -1.0
    best_epoch = 0
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
            batch = {key: value.to(device) for key, value in batch.items()}
            with torch.cuda.amp.autocast(enabled=use_mixed_precision):
                loss = model(**batch).loss
                scaled_loss = loss / accumulation_steps

            scaler.scale(scaled_loss).backward()
            running_loss += float(loss.item())

            should_step = step % accumulation_steps == 0 or step == len(loader)
            if should_step:
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()
                scheduler.step()
                optimizer_steps += 1

        metrics = _evaluate_model(model, tokenizer, valid_examples, model_cfg, device, torch)
        avg_loss = running_loss / max(1, len(loader))
        epoch_record = {
            "epoch": epoch + 1,
            "train_loss": round(avg_loss, 6),
            "optimizer_steps": optimizer_steps,
            "accuracy": round(metrics["accuracy"], 6),
            "precision": round(metrics["precision"], 6),
            "recall": round(metrics["recall"], 6),
            "f1": round(metrics["f1"], 6),
            "label_distribution": metrics["label_distribution"],
            "prediction_distribution": metrics["prediction_distribution"],
        }
        history.append(epoch_record)
        history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")

        print(
            f"epoch {epoch + 1}/{epochs} | "
            f"train_loss={avg_loss:.4f} | "
            f"val_acc={metrics['accuracy']:.4f} | "
            f"val_precision={metrics['precision']:.4f} | "
            f"val_recall={metrics['recall']:.4f} | "
            f"val_f1={metrics['f1']:.4f} | "
            f"pred_dist={metrics['prediction_distribution']} | "
            f"optimizer_steps={optimizer_steps}"
        )

        if metrics["f1"] > best_f1:
            best_f1 = metrics["f1"]
            best_epoch = epoch + 1
            patience = 0
            model.save_pretrained(best_dir)
            tokenizer.save_pretrained(best_dir)
        else:
            patience += 1
            if patience >= early_stopping_patience:
                early_stopped = True
                print(f"early stopping triggered after epoch {epoch + 1}")
                break

    print(
        f"training finished | best_epoch={best_epoch} | "
        f"best_val_f1={best_f1:.4f} | early_stopped={early_stopped} | "
        f"history_file={history_path}"
    )
    return best_dir


def _evaluate_model(model, tokenizer, examples, model_cfg, device, torch) -> dict[str, float]:
    y_true: list[int] = []
    y_pred: list[int] = []
    model.eval()
    for item in examples:
        encoded = tokenizer(
            item.text,
            truncation=True,
            max_length=int(model_cfg.get("max_length", 128)),
            padding=True,
            return_tensors="pt",
        )
        encoded = {key: value.to(device) for key, value in encoded.items()}
        with torch.no_grad():
            label = int(model(**encoded).logits.argmax(dim=-1).item())
        y_true.append(int(item.label))
        y_pred.append(label)

    metrics = binary_metrics(y_true, y_pred)
    metrics["label_distribution"] = dict(sorted(Counter(y_true).items()))
    metrics["prediction_distribution"] = dict(sorted(Counter(y_pred).items()))
    return metrics


def _label_distribution(examples) -> dict[int, int]:
    return dict(sorted(Counter(int(item.label) for item in examples if item.label is not None).items()))
