from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.config import resolve_path
from src.core.events import normalize_event
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
        self.threshold = 0.5
        self.ensemble_bert_weight = 0.5
        self.per_event_thresholds: dict[str, float] = {}
        self.tokenizer_path: Path | None = None
        self._tokenizer: Any = None
        self._model: Any = None
        self._tfidf_model: Any = None

    def load(self) -> None:
        try:
            import joblib
            import torch
            from transformers import AutoModelForSequenceClassification, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("运行环境缺少 PyTorch、transformers 或 joblib，无法加载分类模型。请先安装项目依赖。") from exc

        self._torch = torch
        self.device = torch.device(self.device_name or ("cuda" if torch.cuda.is_available() else "cpu"))
        metadata = self._load_metadata()
        self.threshold = float(metadata["best_threshold"])
        self.ensemble_bert_weight = float(metadata["ensemble_bert_weight"])
        raw_per_event = metadata.get("per_event_thresholds", {})
        self.per_event_thresholds = {
            str(event): float(info["threshold"])
            for event, info in raw_per_event.items()
            if isinstance(info, dict) and "threshold" in info
        }
        tokenizer_path = resolve_path(metadata["tokenizer_path"])
        if not tokenizer_path.exists():
            raise RuntimeError("训练元数据中的分词器路径不存在，请重新训练模型。")
        try:
            self._tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_path), use_fast=False)
        except Exception as exc:
            raise RuntimeError(
                "分词器加载失败。请检查本地预训练模型文件是否完整，并安装 sentencepiece 或 tiktoken 后重试。"
            ) from exc
        try:
            self._model = AutoModelForSequenceClassification.from_pretrained(str(self.model_path), num_labels=2)
        except Exception as exc:
            raise RuntimeError("分类模型权重加载失败。请先完成训练，或检查模型文件路径。") from exc
        tfidf_path = self.model_path / "tfidf_model.joblib"
        if not tfidf_path.exists():
            raise RuntimeError("TF-IDF 融合模型文件缺失，请重新训练模型。")
        self._tfidf_model = joblib.load(tfidf_path)
        self._model.to(self.device)
        self._model.eval()

    def predict(self, text: str, event: str) -> Prediction:
        if self._model is None or self._tokenizer is None or self._tfidf_model is None:
            self.load()

        event = normalize_event(event)

        torch = self._torch
        encoded = self._tokenizer(
            _model_text(text, event),
            truncation=True,
            max_length=self.max_length,
            padding=True,
            return_tensors="pt",
        )
        encoded = {key: value.to(self.device) for key, value in encoded.items()}
        with torch.no_grad():
            logits = self._model(**encoded).logits[0]
            bert_probs = torch.softmax(logits, dim=-1).detach().cpu().tolist()
        tfidf_prob_1 = float(self._tfidf_model.predict_proba([_tfidf_text(text, event)])[0, 1])
        prob_1 = self.ensemble_bert_weight * float(bert_probs[1]) + (1.0 - self.ensemble_bert_weight) * tfidf_prob_1
        prob_0 = 1.0 - prob_1
        event_threshold = self.per_event_thresholds.get(event, self.threshold)
        label = int(prob_1 >= event_threshold)
        return Prediction(
            label=label,
            probabilities={0: prob_0, 1: prob_1},
            model_name=self.model_name,
            text=text,
        )

    def _load_metadata(self) -> dict:
        metadata_path = self.model_path / "training_metadata.json"
        if not metadata_path.exists():
            raise RuntimeError("训练元数据文件缺失，请重新训练模型。")
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError("训练元数据无法读取，请重新训练模型。") from exc
        required_keys = {"best_threshold", "ensemble_bert_weight", "tokenizer_path"}
        if not required_keys.issubset(metadata):
            raise RuntimeError("训练元数据不完整，请重新训练模型。")
        return metadata


def _model_text(text: str, event: str) -> str:
    return text


def _tfidf_text(text: str, event: str) -> str:
    return f"__event_{event}__ {text}"
