from __future__ import annotations

from src.config import load_prompt_config
from src.explain.llm_client import OpenAICompatibleClient
from src.explain.templates import build_prompt
from src.interfaces import Explanation, Prediction, SimilarCase


class LlmExplainer:
    def __init__(self, config: dict, llm_config: dict | None = None, prompt_path: str = "configs/prompt.yaml") -> None:
        self.config = config
        self.prompt = load_prompt_config(prompt_path)
        explain_cfg = llm_config or {}
        self.client = OpenAICompatibleClient(
            model=explain_cfg.get("model", ""),
            base_url=explain_cfg.get("base_url"),
            api_key=explain_cfg.get("api_key"),
        )
        self.temperature = float(explain_cfg.get("temperature", 0.2))

    def explain(
        self,
        text: str,
        prediction: Prediction,
        evidence: list[tuple[str, float]],
        cases: list[SimilarCase],
    ) -> Explanation:
        system = self.prompt.get("system", "")
        template = self.prompt.get("user_template", "{text}")
        user = build_prompt(template, text, prediction, evidence, cases)
        return Explanation(
            text=self.client.complete(system, user, self.temperature),
            evidence=evidence,
            cases=cases,
        )
