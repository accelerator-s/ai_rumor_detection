from __future__ import annotations

from dataclasses import asdict

from src.config import load_config
from src.data.dataset import read_examples
from src.explain.evidence import simple_evidence
from src.explain.generator import LlmExplainer
from src.interfaces import Explanation
from src.models.registry import create_classifier
from src.retrieval.tfidf_retriever import TfidfRetriever


class RumorPipeline:
    def __init__(self, config: dict, with_explainer: bool = True) -> None:
        self.config = config
        self.with_explainer = with_explainer
        self.classifier = create_classifier(config)
        self.classifier.load()
        train_csv = config.get("paths", {}).get("train_csv")
        self.retriever = TfidfRetriever(read_examples(train_csv, config=config)) if train_csv else None

    def predict(self, text: str, explain: bool = True, llm_config: dict | None = None) -> dict:
        prediction = self.classifier.predict(text)
        top_k = int(self.config.get("retrieval", {}).get("top_k", 3))
        cases = self.retriever.search(text, top_k=top_k) if self.retriever else []
        evidence = simple_evidence(text)
        explanation = self._explain(text, prediction, evidence, cases, explain, llm_config)
        return {
            "prediction": asdict(prediction),
            "evidence": evidence,
            "similar_cases": [asdict(case) for case in cases],
            "explanation": asdict(explanation) if explanation else None,
        }

    def _explain(self, text, prediction, evidence, cases, enabled, llm_config) -> Explanation | None:
        if not enabled or not self.with_explainer:
            return None
        explainer = LlmExplainer(self.config, llm_config=llm_config)
        return explainer.explain(text, prediction, evidence, cases)


def build_pipeline(config_path: str = "configs/default.yaml", with_explainer: bool = True) -> RumorPipeline:
    return RumorPipeline(load_config(config_path), with_explainer=with_explainer)
