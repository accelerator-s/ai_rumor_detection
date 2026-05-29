from __future__ import annotations

from src.data.dataset import RumorExample
from src.interfaces import SimilarCase


class TfidfRetriever:
    def __init__(self, examples: list[RumorExample]) -> None:
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.neighbors import NearestNeighbors
        except ImportError as exc:
            raise RuntimeError("Install scikit-learn before using retrieval.") from exc

        self.examples = examples
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        self.matrix = self.vectorizer.fit_transform([item.text for item in examples])
        self.index = NearestNeighbors(metric="cosine", algorithm="brute")
        self.index.fit(self.matrix)

    def search(self, text: str, top_k: int = 3) -> list[SimilarCase]:
        query = self.vectorizer.transform([text])
        distances, indices = self.index.kneighbors(query, n_neighbors=min(top_k, len(self.examples)))
        cases: list[SimilarCase] = []
        for distance, index in zip(distances[0], indices[0]):
            item = self.examples[int(index)]
            cases.append(
                SimilarCase(
                    text=item.text,
                    label=int(item.label),
                    event=item.event,
                    score=1.0 - float(distance),
                )
            )
        return cases

