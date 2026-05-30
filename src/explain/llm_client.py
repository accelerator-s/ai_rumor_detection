from __future__ import annotations

class OpenAICompatibleClient:
    def __init__(self, model: str, base_url: str | None = None, api_key: str | None = None) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("运行环境缺少接口客户端依赖，暂时无法生成解释。") from exc

        self.model = model
        if not self.model:
            raise RuntimeError("请先在“大模型配置”页面选择用于生成解释的模型。")

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
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
