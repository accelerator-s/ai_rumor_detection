# Backend API

Base URL: `http://127.0.0.1:8000`

## GET /health

返回服务状态、pipeline 加载状态和大模型配置摘要。

## POST /predict

只返回分类预测，不生成解释。

```json
{"text": "tweet text"}
```

## POST /explain

返回分类预测、关键证据、相似记录和中文解释。

```json
{"text": "tweet text"}
```

## GET /llm/config

返回本地大模型配置摘要，不返回 API Key 明文。

## POST /llm/config

保存本地大模型配置到 `configs/webui_llm.local.yaml`。

```json
{
  "base_url": "https://example.com/v1",
  "api_key": "sk-...",
  "model": "model-name",
  "temperature": 0.2
}
```

## GET /llm/models

使用已保存配置拉取模型列表。

## POST /llm/models

使用请求体里的 Base URL 和 API Key 临时拉取模型列表。

```json
{
  "base_url": "https://example.com/v1",
  "api_key": "sk-..."
}
```

