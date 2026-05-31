from __future__ import annotations

import random
from pathlib import Path

from src.config import resolve_path
from src.data.dataset import export_cleaned_datasets, read_examples
from src.evaluation.metrics import binary_metrics
from src.training.checkpoint import checkpoint_path


def train(config: dict) -> Path:
    try:
        import torch
        from torch.utils.data import DataLoader
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("Install torch and transformers before training.") from exc

    seed = int(config.get("seed", 42))
    random.seed(seed)
    torch.manual_seed(seed)

    paths = config["paths"]
    model_cfg = config["model"]
    train_cfg = config["training"]

    export_cleaned_datasets(config)
    examples = read_examples(paths["train_csv"], config=config)
    random.shuffle(examples)
    valid_size = max(1, int(len(examples) * 0.1))
    valid_examples = examples[:valid_size]
    train_examples = examples[valid_size:]

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

    best_f1 = -1.0
    best_dir = checkpoint_path(paths["checkpoint_dir"], "best")

    for _ in range(int(train_cfg.get("epochs", 3))):
        model.train()
        for batch in loader:
            batch = {key: value.to(device) for key, value in batch.items()}
            loss = model(**batch).loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        metrics = _evaluate_model(model, tokenizer, valid_examples, model_cfg, device, torch)
        if metrics["f1"] > best_f1:
            best_f1 = metrics["f1"]
            model.save_pretrained(best_dir)
            tokenizer.save_pretrained(best_dir)

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
    return binary_metrics(y_true, y_pred)

