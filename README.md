# 可解释的谣言检测系统

本项目是《人工智能导论》课程大作业“可解释的谣言检测”的工程实现。目标是在给定推文文本后，输出二分类检测结果，并给出一段可读的判断依据。

分类标签定义如下：

- `0`：非谣言
- `1`：谣言

项目以 `data/train.csv` 作为训练集，以 `data/val.csv` 作为官方验证集。数据字段包括 `id`、`text`、`label`、`event`。

## 设计目标

本项目优先满足以下目标：

1. **控制过拟合风险**：谣言检测容易受到具体事件、人名、地名和话题标签影响。由于训练数据规模有限，模型可能记住训练集中出现过的事件表面特征，因此需要在文本归一化、验证集评估、正则化训练和错误分析中持续关注过拟合问题。
2. **本地可训练**：训练过程面向普通笔记本电脑独立显卡设计，控制模型规模、序列长度、batch size 和依赖复杂度，保证合理运行时间。
3. **检测与解释分层**：分类模型负责给出标签和概率，解释模块负责把模型证据、相似样本和文本特征组织成自然语言依据。
4. **仓库可复现**：训练、评测、预测和解释流程均通过脚本运行，最终结果以 `val.csv` 上的准确率作为主要检测指标。

## 技术路线

系统采用“深度分类模型 + 轻量检索 + 解释生成”的复合结构。

### 1. 文本预处理与归一化

推文文本包含 URL、用户提及、转发标记、话题标签、HTML 转义字符等噪声。预处理模块会进行统一归一化：

- 将 URL、用户提及、转发标记归一为稳定占位符；
- 处理 HTML 转义字符；
- 保留否定词、情绪词、标点和话题标签中的有效语义；
- 构造“原始文本视图”和“归一化文本视图”，减少模型对单一事件实体的依赖。

归一化文本视图不会简单删除所有实体信息，而是对强事件绑定的片段进行规范化。这样既避免模型死记硬背具体事件，也尽量保留谣言检测所需的语义线索。

### 2. 分类模型

主分类模型采用面向英文短文本的预训练语言模型 `vinai/bertweet-base` 进行二分类微调。训练时会在本项目数据上更新分类层和模型参数，使模型学习谣言检测任务本身。

训练策略包括：

- 最大序列长度控制在短推文适合的范围内；
- 使用较小 batch size、梯度累积和混合精度训练，适配笔记本 GPU；
- 使用验证集监控 early stopping，避免小数据集过拟合；
- 记录 accuracy、precision、recall、F1 和推理耗时；
- 保存最优模型权重和 tokenizer 配置。

### 3. 模型评估与错误分析

评估模块负责在训练完成后读取模型预测结果，计算官方验证集指标，并结合 `event` 字段进行错误分析。

该部分用于回答三个层次的问题：

- **整体分类效果**：模型在 `val.csv` 上的 Accuracy、Precision、Recall、F1 表现如何；
- **错误分布**：错误样本主要集中在哪些 `event`、标签类别或文本模式中；
- **过拟合风险**：训练集与验证集表现是否差距过大，是否存在对特定事件记忆过强的迹象，从而为调整文本归一化、正则化和 early stopping 提供依据。

最终成绩仍以 `val.csv` 上的分类准确率为准。

### 4. 相似案例检索

相似案例检索用于从训练集中找到与当前输入表达接近的样本，为解释模块提供可参考的历史案例。该模块采用成熟文本检索库实现，保证结果稳定、依赖清晰，并便于在报告中解释检索逻辑。

默认方案如下：

- 使用 `scikit-learn` 的 `TfidfVectorizer` 表示训练集文本；
- 使用余弦相似度或 `NearestNeighbors` 进行相似度计算；
- 召回 Top-K 个相似训练样本；
- 将相似样本的文本、标签和相似度提供给解释模块。

该模块不是外部事实核查系统，而是“相似案例参考”。它的作用是帮助解释模块说明当前文本与训练集中哪些表达模式接近，同时避免解释只依赖模型标签本身。

### 5. 可解释性生成

解释模块由两部分组成：

1. **模型证据提取**：从分类模型中提取对预测有贡献的文本片段。优先采用输入扰动法，即遮蔽或替换部分 token，观察目标类别概率变化，从而估计关键词或短语的重要性。
2. **大语言模型解释生成**：综合预测标签、置信度、重要片段和相似案例，生成一段面向用户的判断依据。

解释文本通过 SJTU API 的 OpenAI 兼容接口调用大语言模型生成。大语言模型只负责组织表达，不直接决定分类标签。最终解释应围绕可观察证据展开，避免把相似案例描述成外部事实证据。

### 6. WebUI 展示内容

WebUI 作为独立的交互展示层，调用后端预测接口，展示单条输入文本的检测结果、解释依据和服务状态。

界面需要实现以下展示内容：

- **大模型配置区**：填写 OpenAI 兼容接口的 Base URL 和 API Key，自动获取可用模型列表并选择模型；
- **文本输入区**：提供推文文本输入框、提交按钮和示例文本入口；
- **预测结果区**：展示预测标签、谣言概率、非谣言概率、置信度和模型名称；
- **解释依据区**：展示自然语言判断依据，并区分模型证据、输入文本片段和相似案例参考；
- **关键证据区**：展示对预测贡献较高的 token、短语或文本片段；
- **相似案例区**：展示 Top-K 相似训练样本，包括样本文本、标签和相似度；
- **请求状态区**：展示模型是否已加载、后端服务是否可用、预测耗时和错误信息；
- **结果导出区**：支持复制或保存当前预测结果，便于写入实验记录和报告。

大模型配置保存到 `configs/webui_llm.local.yaml`，该文件已加入 `.gitignore`，不提交到仓库。`configs/default.yaml` 只保存训练、评估和路径相关配置。

## 计划目录结构

当前阶段先确定工程说明，后续实现会按如下结构组织：

```text
.
├── data/
│   ├── train.csv                  # 训练集
│   └── val.csv                    # 官方验证集
├── configs/
│   ├── default.yaml               # 通用配置：路径、随机种子、模型选择、训练参数
│   └── prompt.yaml                # 解释生成相关配置
├── docs/                          # 参考文档及报告文档
├── models/
│   └── pretrained/
│       └── .gitkeep               # 保留本地预训练模型缓存目录
├── src/
│   ├── interfaces.py              # Classifier、Retriever、Explainer 等接口定义
│   ├── config.py                  # 配置读取、默认值合并和路径检查
│   ├── pipeline.py                # 端到端预测流程编排
│   ├── data/
│   │   ├── dataset.py             # Dataset/DataLoader 与 CSV 读取
│   │   ├── preprocess.py          # 文本清洗、URL/用户提及归一化
│   │   └── splits.py              # 训练内验证划分与 event 分组工具
│   ├── models/
│   │   ├── transformer.py         # BERTweet 分类模型封装
│   │   └── registry.py            # 根据配置创建模型
│   ├── training/
│   │   ├── trainer.py             # 训练循环、loss、optimizer、early stopping
│   │   └── checkpoint.py          # 最优模型保存与加载
│   ├── evaluation/
│   │   ├── metrics.py             # accuracy、precision、recall、F1 等指标
│   │   ├── evaluator.py           # val.csv 评估流程
│   │   └── event_analysis.py      # 按 event 统计错误分布
│   ├── retrieval/
│   │   └── tfidf_retriever.py     # 基于 scikit-learn 的相似案例检索
│   ├── explain/
│   │   ├── evidence.py            # 输入扰动、关键词贡献度等模型证据
│   │   ├── generator.py           # 解释文本生成入口
│   │   ├── llm_client.py          # OpenAI 兼容接口封装
│   │   └── templates.py           # 不同解释模式的模板
│   ├── train.py                   # 训练入口
│   ├── evaluate.py                # val.csv 与事件维度评测入口
│   ├── predict.py                 # 单条文本预测入口
│   └── webui/
│       ├── main.py                # 一次启动后端服务和前端界面
│       ├── backend/
│       │   ├── routes.py          # /health、/predict、/explain、/llm/* 路由
│       │   ├── services.py        # 参数校验、pipeline 调用和配置读写
│       │   ├── state.py           # 服务启动时加载并缓存 pipeline
│       │   └── errors.py          # 统一异常类型
│       └── frontend/
│           ├── interface.py       # Gradio 界面和事件注册
│           ├── api.py             # 后端接口请求封装
│           ├── components/        # 页面区域定义
│           └── formatters.py      # 展示格式化
├── outputs/
│   ├── checkpoints/               # 模型权重和 tokenizer 文件
│   ├── metrics/                   # 评测结果 JSON/CSV
│   └── predictions/               # val.csv 预测明细与解释结果
├── requirements.txt               # 通用 Python 依赖，PyTorch 单独安装
├── README.md                      # 工程说明
└── report.pdf                     # 最终报告
```

## 代码组织要求

代码实现遵循以下代码组织原则：

- 单个源代码文件不宜过长，原则上不超过 1000 行；
- 文件之间责任清晰，避免把数据处理、模型训练、评测、解释生成和界面逻辑混在同一个文件中；
- 核心模块通过明确接口连接，例如 `Classifier`、`Retriever`、`Explainer`、`Predictor` 等；
- 训练、评测、预测和解释流程应能分别独立运行，也能在端到端入口中组合调用；
- 训练模块只负责参数更新，评估模块只负责指标统计，解释模块只负责组织预测依据，三者通过模型输出和结构化结果连接；
- 配置项集中放在 `configs/` 中，避免在多个脚本中散落硬编码参数；
- 对外部模型接口和本地模型推理做封装，避免业务代码直接依赖具体 API 调用细节。

## 运行方式

建议使用 Python 3.11。项目可以在 CPU 环境下完成单条推理和小规模调试；若要高效训练分类模型，建议使用支持 CUDA 的 NVIDIA GPU，并安装与本机显卡驱动和 CUDA 环境匹配的 PyTorch 版本。

PyTorch 需要根据本机 CPU/CUDA 环境单独安装。安装时应在 PyTorch 官网选择当前 Stable 版本，并匹配本机操作系统、Python 版本和计算平台。示例命令如下，实际安装命令以 PyTorch 官网为准：

```bash
# CPU 版本
pip install torch --index-url https://download.pytorch.org/whl/cpu

# CUDA 版本，适用于支持 CUDA 的 NVIDIA GPU 环境
# 将 cuXXX 替换为 PyTorch 官网推荐的 CUDA wheel 源，例如 cu128
pip install torch --index-url https://download.pytorch.org/whl/cuXXX
```

```bash
# 安装依赖
pip install -r requirements.txt

python - <<'PY'
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="vinai/bertweet-base",
    local_dir="models/pretrained",
)
PY

# 训练分类模型
python -m src.train --config configs/default.yaml

# 在 val.csv 上评测
python -m src.evaluate --config configs/default.yaml --split val

# 单条文本预测
python -m src.predict --text "input tweet here"

# 启动 WebUI
python -m src.webui.main
```

WebUI 后端提供 `/llm/config` 和 `/llm/models` 路由，用于保存本地大模型配置和拉取模型列表。

## 评测指标

分类性能：

- Accuracy：总体预测正确的比例，对应作业评分中的 `val.csv` 分类准确率；
- Precision：模型预测为谣言的样本中，实际真的是谣言的比例，用于观察误报情况；
- Recall：所有真实谣言样本中，被模型成功找出的比例，用于观察漏报情况；
- F1：Precision 和 Recall 的综合指标，适合在类别不均衡时辅助判断模型效果；
- Per-event metrics：按 `event` 分组统计指标，用于分析模型在哪些事件上更容易出错；
- Inference time：单条或批量预测耗时，用于说明运行时间是否合理。

解释质量：

- 是否与模型预测标签一致；
- 是否引用了输入文本中的具体证据；
- 是否区分“模型证据”“相似案例”和“事实结论”；
- 是否避免无依据扩写。
