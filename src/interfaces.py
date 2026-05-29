from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


LABEL_NAMES = {0: "非谣言", 1: "谣言"}


@dataclass(slots=True)
class Prediction:
    label: int
    probabilities: dict[int, float]
    model_name: str
    text: str = ""

    @property
    def confidence(self) -> float:
        return self.probabilities.get(self.label, 0.0)

    @property
    def label_name(self) -> str:
        return LABEL_NAMES.get(self.label, str(self.label))


@dataclass(slots=True)
class SimilarCase:
    text: str
    label: int
    event: str
    score: float

    @property
    def label_name(self) -> str:
        return LABEL_NAMES.get(self.label, str(self.label))


@dataclass(slots=True)
class Explanation:
    text: str
    evidence: list[tuple[str, float]] = field(default_factory=list)
    cases: list[SimilarCase] = field(default_factory=list)


class Classifier(Protocol):
    model_name: str

    def predict(self, text: str) -> Prediction:
        ...


class Retriever(Protocol):
    def search(self, text: str, top_k: int = 3) -> list[SimilarCase]:
        ...


class Explainer(Protocol):
    def explain(
        self,
        text: str,
        prediction: Prediction,
        evidence: list[tuple[str, float]],
        cases: list[SimilarCase],
    ) -> Explanation:
        ...

