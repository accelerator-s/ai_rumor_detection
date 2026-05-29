from __future__ import annotations

from pathlib import Path
from typing import Any

from src.config import resolve_path
from src.interfaces import Prediction


class BertweetClassifier:
    def __init__(
        self,
        model_path: str | Path,
        model_name: str = "vinai/bertweet-base",
        max_length: int = 128,
        device: str | None = None,
    ) -> None:
        self.model_path = resolve_path(model_path)
        self.model_name = model_name
        self.max_length = max_length
        self.device_name = device
        self._tokenizer: Any = None
        self._model: Any = None

    def load(self) -> None:
        try:
            import torch
            from transformers import AutoModelForSequenceClassification, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("Install torch and transformers before loading the classifier.") from exc

        self._torch = torch
        self.device = torch.device(self.device_name or ("cuda" if torch.cuda.is_available() else "cpu"))
        self._tokenizer = AutoTokenizer.from_pretrained(str(self.model_path), use_fast=False)
        self._model = AutoModelForSequenceClassification.from_pretrained(str(self.model_path), num_labels=2)
        self._model.to(self.device)
        self._model.eval()

    def predict(self, text: str) -> Prediction:
        if self._model is None or self._tokenizer is None:
            self.load()

        torch = self._torch
        encoded = self._tokenizer(
            text,
            truncation=True,
            max_length=self.max_length,
            padding=True,
            return_tensors="pt",
        )
        encoded = {key: value.to(self.device) for key, value in encoded.items()}
        with torch.no_grad():
            logits = self._model(**encoded).logits[0]
            probs = torch.softmax(logits, dim=-1).detach().cpu().tolist()
        label = int(max(range(len(probs)), key=probs.__getitem__))
        return Prediction(
            label=label,
            probabilities={0: float(probs[0]), 1: float(probs[1])},
            model_name=self.model_name,
            text=text,
        )

