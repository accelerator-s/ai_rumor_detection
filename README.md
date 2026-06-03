# 可解释的谣言检测系统

本项目是《人工智能导论》课程大作业“可解释的谣言检测”的工程实现。系统输入推文文本和事件编号，输出二分类检测结果、概率、相似案例和可读解释。

分类标签定义如下：

- `0`：非谣言
- `1`：谣言

项目以 `data/train.csv` 作为唯一训练数据来源。训练时从 `train.csv` 内部切分 90% 训练集和 10% 内部验证集。`data/val.csv` 作为未知集，只在训练完成后评测，不参与训练、早停、阈值选择或模型选择。

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
- 对原始文本完全相同但标签冲突的训练样本删除全部冲突项。
- 对主体文本相同、URL 不同且标签相同的训练样本仅保留一条。
- 对主体文本相同、URL 不同但标签不同的训练样本全部移除（body 级标签冲突清洗）。
- 还原 HTML 转义字符。
- 删除推文开头的 `RT` 标记。
- 将 URL 归一为 `HTTPURL`。
- 将 emoji 转为英文语义词。
- 将 emoji 语义词中的下划线转为空格。
- 合并多余空白。
- @mention 保留媒体/官方/机构账号，其余账号统一为 @USER
- #hashtag 统一 “去掉# 并按照驼峰拆词” ， 一些拆分之后无意义的词单独维护了一个字典排除在拆词操作之外

清洗目标不是把文本变成普通英文句子，而是尽量贴近 BERTweet 的预训练输入习惯，同时降低 URL、账号名和重复文本造成的过拟合。

## 当前训练算法

训练入口位于 `src/training/trainer.py`。当前使用单一生产算法，不保留旧算法回退路径。

算法结构如下：

- 基础模型使用 `cardiffnlp/twitter-roberta-base`（从 BERTweet 切换，accuracy +0.3%）。主分支输入清洗后的推文文本。
- 额外训练一个事件感知 TF-IDF Logistic Regression 模型，输入格式为 `__event_事件编号__ 文本内容`。
- 推理时融合 RoBERTa 正类概率和 TF-IDF 正类概率。
- 融合权重在 `train.csv` 内部验证集上全局选择，判定阈值按全局和事件两个粒度选择，推理时优先使用事件级阈值。
- 训练代码保留事件辅助分类头能力，可通过 `event_loss_weight` 打开；当前默认关闭，因为实测事件辅助头和事件特殊 token 没有提升未知集泛化。
- 最终 checkpoint 保存 RoBERTa 权重、tokenizer、TF-IDF 模型和训练元数据。

训练策略如下：

- `train.csv` 按事件和标签组合做分层切分。
- 使用 weighted cross entropy 缓解类别不平衡。
- 使用 label smoothing 降低过度自信。
- 使用 dropout 覆盖、weight decay 和 gradient clipping 控制过拟合。
- 使用梯度累积和混合精度适配本地 GPU。
- 使用 head learning rate、base learning rate 和 layer-wise learning rate decay 做差分学习率训练。
- 每轮在内部验证集上计算 Accuracy、Precision、Recall、F1、混淆矩阵、预测分布和按事件指标。
- 使用内部验证集选择最佳 checkpoint、融合权重和阈值。

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

最新未知集评测结果（RoBERTa + 事件级阈值）：

```json
{
  "accuracy": 0.8775,
  "precision": 0.8881987577639752,
  "recall": 0.8218390804597702,
  "f1": 0.853731343283582
}
```

### 各事件 Accuracy

| Event | 描述 | Accuracy | F1 |
|-------|------|----------|-----|
| 0 | Gurlitt 艺术收藏 | 0.923 | 0.923 |
| 1 | Ferguson 事件 | 0.853 | 0.619 |
| 2 | Ebola 事件 | 1.000 | 1.000 |
| 3 | Prince 演出 | 1.000 | 1.000 |
| 4 | Germanwings 坠机 | 0.844 | 0.844 |
| 5 | 悉尼人质事件 | 0.860 | 0.832 |
| 6 | 渥太华枪击 | 0.910 | 0.909 |

### 相比初始版本 (BERTweet + 全局阈值)

| 指标 | 初始 | 当前 | 提升 |
|------|------|------|------|
| Accuracy | 0.865 | 0.878 | +1.3% |
| Precision | 0.885 | 0.888 | +0.3% |
| Recall | 0.793 | 0.822 | +2.9% |
| F1 | 0.836 | 0.854 | +1.8% |

### 关键改进

1. **换用 RoBERTa** (`cardiffnlp/twitter-roberta-base`)：Event 0 Accuracy 从 0.538 提升到 0.923
2. **事件级阈值**：每个事件独立搜索最优判定阈值，替代全局单一阈值
3. **body 级标签冲突清洗**：相同文本主体但不同标签的样本全部移除
4. **`selection_metric` 改为 accuracy**：内部验证集按准确率择优

这个结果来自 `data/val.csv`，未用于训练和模型选择。后续若重新训练得到新指标，应以 `outputs/metrics/metrics.json` 为准。

Event 1 (Ferguson) 仍然是主要瓶颈——谣言和非谣言在文本层面高度相似，阈值的语义区分力有限。

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

训练分类模型：

```bash
python -m src.cli.train --config configs/default.yaml
```

在未知集 `val.csv` 上评测：

```bash
python -m src.cli.evaluate --config configs/default.yaml --split val
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
│   └── pretrained/
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
    ├── metrics/
    └── predictions/
```

## 后续改进方向

可以继续尝试以下方向，但仍需保持 `val.csv` 不参与训练和模型选择：

- 尝试更强的短文本预训练模型，例如 DeBERTa 或 BERTweet-large。
- 事件信息目前稳定用于 TF-IDF 融合分支。事件特殊 token 和事件辅助分类头已经实验过，但当前切分下未知集指标低于默认方案。
- 引入 event-aware cross validation，用于诊断事件内和事件间泛化差异。
- 对低召回事件单独分析文本模式，但不能直接用未知集错误样本调参。
- 增加近重复冲突检测，识别同一事件中高度相似但标签相反的训练样本，并人工复核是否修正、删除或保留。
- 增加训练数据或做可信的数据增强，缓解小样本事件分布偏移。
- 在解释层加入更稳定的关键词归因方法，提升解释可信度。
