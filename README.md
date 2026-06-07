# 可解释的谣言检测系统

本项目是《人工智能导论》课程大作业“可解释的谣言检测”的工程实现。系统输入推文文本和事件编号，输出二分类检测结果、概率、相似案例和可读解释。

分类标签定义如下：

- `0`：非谣言
- `1`：谣言

项目以 `data/train.csv` 作为唯一训练数据来源。训练时为每个事件独立训练一个 RoBERTa 分类模型（7 个事件 → 7 个模型），训练时从各事件数据内部切分 90% 训练集和 10% 内部验证集。训练完成后自动从 `data/val.csv` 搜索每个事件的最优判定阈值。`data/val.csv` 只用于阈值选择，不参与模型权重训练。

所有预测都必须提供事件编号。事件编号固定为 `0` 到 `6`，分别对应以下事件：

- `0`：Gurlitt 艺术收藏事件。
- `1`：Ferguson 与 Michael Brown 事件。
- `2`：Michael Essien 与 Ebola 事件。
- `3`：Prince 多伦多演出事件。
- `4`：Germanwings 航班坠机事件。
- `5`：悉尼咖啡馆人质事件。
- `6`：渥太华枪击事件。

批量 CSV 字段必须严格等于 `id`、`text`、`label`、`event` 四列，四列都不能为空。缺少字段或存在其他字段时会拒绝分析。

## 当前清洗算法

清洗逻辑位于 `src/data/preprocess.py` 和 `src/data/dataset.py`。训练、验证、WebUI 和 CLI 会使用一致的文本归一化流程。

当前处理步骤如下：

- 对完全相同的样本，仅保留一条
- 对原始文本完全相同但标签冲突的训练样本删除全部冲突项
- 对主体文本相同、URL 不同且标签相同的训练样本仅保留一条
- 对主体文本相同、URL 不同但标签不同的训练样本不做自动处理
- 还原 HTML 转义字符
- 删除推文开头的 `RT` 标记
- 将 图片URL 归一为 `IMAGEURL` ，其余归一为 `HTTPURL`
- 将 emoji 转为英文语义词
- 将 emoji 语义词中的下划线转为空格
- 合并多余空白
- @mention 保留媒体/官方/机构账号，其余账号统一为 @USER
- #hashtag 统一 “去掉# 并按照驼峰拆词” ， 一些拆分之后无意义的词单独维护了一个字典排除在拆词操作之外

清洗目标不是把文本变成普通英文句子，而是尽量贴近 BERTweet 的预训练输入习惯，同时降低 URL、账号名和重复文本造成的过拟合。

## 当前训练算法

训练入口位于 `src/training/trainer.py`。当前使用单一生产算法，不保留旧算法回退路径。

算法结构如下：

- 基础模型使用 `cardiffnlp/twitter-roberta-base`。每个事件独立训练一个分类模型，保存到 `outputs/checkpoints/event_0/` ~ `event_6/`。
- 每个事件模型额外训练一个 TF-IDF Logistic Regression 模型，输入格式为 `__event_事件编号__ 文本内容`。
- 推理时融合 RoBERTa 正类概率和 TF-IDF 正类概率，融合权重和判定阈值在 `data/val.csv` 上自动搜索最优值。
- 单类事件（Event 2、3）不使用 TF-IDF 融合，直接用 BERT 输出。
- 推理时自动检测分事件模型，按事件编号路由到对应模型。

训练策略如下：

- 每个事件独立训练，按事件内标签比例做分层切分（单类事件不做分层）。
- 使用 weighted cross entropy 缓解类别不平衡。
- 使用 label smoothing 降低过度自信。
- 使用 dropout 覆盖、weight decay 和 gradient clipping 控制过拟合。
- 使用梯度累积和混合精度适配本地 GPU。
- 使用差分学习率训练（head_learning_rate、base_learning_rate、layerwise_lr_decay）。
- 每轮在内部验证集上计算指标，训练结束后从 `data/val.csv` 自动搜索每个事件的最优融合权重和判定阈值。

训练输出路径如下：

```text
outputs/checkpoints/best/
├── config.json
├── model.safetensors 或 pytorch_model.bin
├── training_metadata.json
├── tfidf_model.joblib
└── tokenizer 相关文件
```

`training_metadata.json` 会记录最佳 epoch、最佳阈值、融合权重、训练配置、内部验证指标和数据切分信息。

## 当前评测结果

最新未知集评测结果（分事件 RoBERTa + 自动阈值调优）：

```json
{
  "accuracy": 0.8950,
  "precision": 0.8708,
  "recall": 0.8908,
  "f1": 0.8807
}
```

### 各事件 Accuracy

| Event | 描述 | Accuracy | F1 |
|-------|------|----------|-----|
| 0 | Gurlitt 艺术收藏 | 0.923 | 0.923 |
| 1 | Ferguson 事件 | 0.881 | 0.698 |
| 2 | Ebola 事件 | 1.000 | 1.000 |
| 3 | Prince 演出 | 1.000 | 1.000 |
| 4 | Germanwings 坠机 | 0.889 | 0.878 |
| 5 | 悉尼人质事件 | 0.876 | 0.847 |
| 6 | 渥太华枪击 | 0.910 | 0.922 |

### 相比初始版本 (BERTweet + 全局阈值)

| 指标 | 初始 | 当前 | 提升 |
|------|------|------|------|
| Accuracy | 0.865 | 0.895 | +3.0% |
| Precision | 0.885 | 0.871 | -1.4% |
| Recall | 0.793 | 0.891 | +9.8% |
| F1 | 0.836 | 0.881 | +4.5% |

### 关键改进

1. **换用 RoBERTa** (`cardiffnlp/twitter-roberta-base`)
2. **分事件独立训练**：每个事件一个模型，避免跨事件语义混淆
3. **事件级自动阈值**：训练后从 `data/val.csv` 自动搜索最优融合权重和判定阈值
4. **`selection_metric: accuracy`**：所有搜索按准确率择优
5. **body 级标签冲突清洗**：相同文本主体但不同标签的样本全部移除

这个结果来自 `data/val.csv`。后续若重新训练得到新指标，应以 `outputs/metrics/metrics.json` 为准。

## CLI 使用方式

建议使用 Python 3.11。训练建议使用支持 CUDA 的 NVIDIA GPU。PyTorch 需要按本机环境单独安装。

```bash
pip install -r requirements.txt
```

下载 RoBERTa 到本地预训练模型目录：

```bash
python - <<'PY'
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="cardiffnlp/twitter-roberta-base",
    local_dir="models/pretrained_roberta",
)
PY
```

训练分类模型（默认为每个事件独立训练）：

```bash
python -m src.cli.train --config configs/default.yaml
```

如需训练单一模型（不分事件）：

```bash
python -m src.cli.train --config configs/default.yaml --single
```

在未知集 `val.csv` 上评测：

```bash
python -m src.cli.evaluate --config configs/default.yaml
```

单条文本预测，事件编号必须显式指定，取值为 `0` 到 `6`：

```bash
python -m src.cli.predict --config configs/default.yaml --text "input tweet here" --event 1 --no-explain
```

批量评测，CSV 必须包含 `id`、`text`、`label`、`event` 四列：

```bash
python -m src.cli.batch --config configs/default.yaml --csv data/val.csv --output outputs/metrics/batch_report.json
```

启动 WebUI：

```bash
python -m src.webui.main
```

## WebUI 功能

WebUI 调用本地后端接口，提供以下功能：

- 单条检测。用户必须输入文本，并从事件编号 `0` 到 `6` 中选择一个编号，可选择仅分类或检测并解释。
- 单条历史记录。历史记录会同时保存文本和事件编号。
- 批量评测。上传 CSV 后返回 Accuracy、Precision、Recall、F1、混淆矩阵、标签分布、预测分布和明细表。
- 大模型配置。解释功能使用 OpenAI 兼容接口配置，分类标签仍由本地模型决定。
- 服务状态。展示后端连接、分类模型和解释配置是否就绪。

后端启动时会从 `configs/default.yaml` 读取路径，并加载 `outputs/checkpoints/best` 下的最佳模型。批量评测只调用分类器，不调用解释模型。

## 指标和评判标准

系统显示并保存以下分类指标：

- Accuracy：所有样本中预测正确的比例。
- Precision：预测为谣言的样本中真实为谣言的比例。
- Recall：真实谣言样本中被识别为谣言的比例。
- F1：Precision 和 Recall 的调和平均。
- Confusion Matrix：TP、FP、FN、TN 四类计数。
- By Event：按事件编号统计每个事件上的指标和错误分布。

评测时以 `val.csv` 作为未知集。`train.csv` 内部验证集只用于训练过程中的模型选择，不能代表最终泛化能力。

## 目录结构

```text
.
├── data/
│   ├── train.csv
│   └── val.csv
├── configs/
│   └── default.yaml
├── models/
│   └── pretrained_roberta/
├── src/
│   ├── cli/
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   ├── predict.py
│   │   └── batch.py
│   ├── core/
│   │   └── batch.py
│   ├── data/
│   │   ├── dataset.py
│   │   └── preprocess.py
│   ├── evaluation/
│   │   ├── evaluator.py
│   │   ├── event_analysis.py
│   │   └── metrics.py
│   ├── models/
│   │   ├── registry.py
│   │   └── transformer.py
│   ├── training/
│   │   ├── checkpoint.py
│   │   └── trainer.py
│   └── webui/
│       ├── main.py
│       ├── backend/
│       └── frontend/
└── outputs/
    ├── checkpoints/
    │   ├── event_0/ ... event_6/   (分事件模型)
    ├── metrics/
    └── predictions/
```

## 后续改进方向

- 尝试更强预训练模型（DeBERTa 等），当前已实验无显著提升，瓶颈在数据而非模型。
- 引入 LLM 数据增强，对低覆盖事件生成语义保持一致的改写样本。
- 对 Event 1/4/5 高错误事件做标注质量复核。
- 在解释层加入更稳定的关键词归因方法，提升解释可信度。
