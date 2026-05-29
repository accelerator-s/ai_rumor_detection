from __future__ import annotations

import os


class OpenAICompatibleClient:
    def __init__(self, model: str, base_url: str | None = None, api_key: str | None = None) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install openai before generating explanations.") from exc

        self.model = model or os.getenv("SJTU_MODEL", "")
        if not self.model:
            raise RuntimeError("Select an explanation model in WebUI first.")

        self.client = OpenAI(
            api_key=api_key or os.getenv("SJTU_API_KEY"),
            base_url=base_url or os.getenv("SJTU_BASE_URL"),
        )

    def complete(self, system: str, user: str, temperature: float = 0.2) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content or ""
