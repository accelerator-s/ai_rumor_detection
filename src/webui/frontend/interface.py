from __future__ import annotations

import json

from src.webui.frontend.api import BackendClient
from src.webui.frontend.formatters import format_cases, format_prediction


def create_interface(client: BackendClient):
    try:
        import gradio as gr
    except ImportError as exc:
        raise RuntimeError("Install gradio before starting the frontend.") from exc

    saved = client.llm_config()

    def run(text: str):
        result = client.explain(text)
        explanation = (result.get("explanation") or {}).get("text") or ""
        return format_prediction(result), explanation, format_cases(result), json.dumps(result, ensure_ascii=False, indent=2)

    def fetch_models(base_url: str, api_key: str):
        models = client.models(base_url, api_key)
        value = models[0] if models else ""
        return gr.update(choices=models, value=value)

    def save_config(base_url: str, api_key: str, model: str, temperature: float):
        payload = {
            "base_url": base_url,
            "model": model,
            "temperature": temperature,
        }
        if api_key:
            payload["api_key"] = api_key
        result = client.save_llm_config(payload)
        return f"已保存: {result.get('model', '')}"

    with gr.Blocks(title="谣言检测") as demo:
        gr.Markdown("# 可解释的谣言检测")
        with gr.Accordion("大模型配置", open=not saved.get("model")):
            base_url = gr.Textbox(label="Base URL", value=saved.get("base_url", ""))
            api_key = gr.Textbox(label="API Key", type="password")
            models = gr.Dropdown(label="模型", choices=[], value=saved.get("model") or None)
            temperature = gr.Slider(label="Temperature", minimum=0, maximum=1, step=0.1, value=float(saved.get("temperature", 0.2)))
            fetch_button = gr.Button("获取模型列表")
            save_button = gr.Button("保存配置")
            config_status = gr.Textbox(label="配置状态", interactive=False)
            fetch_button.click(fetch_models, inputs=[base_url, api_key], outputs=models)
            save_button.click(save_config, inputs=[base_url, api_key, models, temperature], outputs=config_status)

        text = gr.Textbox(label="推文文本", lines=5)
        button = gr.Button("检测")
        pred = gr.Textbox(label="预测结果", lines=5)
        explanation = gr.Textbox(label="判断依据", lines=6)
        cases = gr.Textbox(label="相似案例", lines=8)
        raw = gr.JSON(label="原始结果")
        button.click(run, inputs=text, outputs=[pred, explanation, cases, raw])

    return demo

