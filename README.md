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

通过`src/data/preprocess.py`实现。后续需要参考 BERTweet 的预训练方式，对训练、验证和在线输入统一执行：

- 还原 HTML 转义字符，统一空白和特殊标点；
- 删除开头的 `RT`，将 URL 和用户提及分别归一为 `HTTPURL`、`@USER`；
- 将 emoji 转写为语义标记，例如 `😢` 转为 `:crying_face:`，而不是直接过滤；
- 保留否定词、大小写、话题标签和有意义的标点；
- 检查重复文本、标签冲突以及训练集与验证集之间的重复样本。

例如，`data/train.csv` 中的：

```text
#Ferguson PD beat, &amp; charged innocent man with "Property Damage" for bleeding on officer's clothes @YourAnonNews  http://t.co/cdyvEIzZRw
```

预期归一化为：

```text
#Ferguson PD beat, & charged innocent man with "Property Damage" for bleeding on officer's clothes @USER HTTPURL
```

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

### 6. WebUI 展示与模型衔接

WebUI 是纯静态 SPA 展示层，调用本地后端接口组织单条检测、批量评测、大模型配置和服务状态四类能力：

- **单条检测**：支持“仅分类”或“检测并解释”，展示分类标签、置信度、关键证据词、Top-K 相似案例和 JSON 导出；
- **批量评测**：导入包含 `text` 列的 CSV，后端逐条分类并返回结果；存在 `label` 列时同步展示 Accuracy、Precision、Recall、F1、混淆矩阵、分布统计和错误明细；
- **大模型配置**：保存 OpenAI 兼容接口的 Base URL、API Key、模型和温度到 `configs/explain_llm.local.yaml`，供 CLI 和 WebUI 的解释生成共同使用；若旧版 `configs/webui_llm.local.yaml` 仍存在且新文件不存在，会继续兼容读取；
- **服务状态**：以监控面板展示后端连接、分类模型和解释配置的就绪情况；模型权重未加载时禁用单条和批量操作。

后端启动时通过 `configs/default.yaml` 自动衔接训练权重：`src.cli.train` 默认把最佳 checkpoint 保存到 `outputs/checkpoints/best`，`src.webui.main` 启动后从 `paths.checkpoint_dir` 查找最新的 `best*` 目录并缓存为 `RumorPipeline`。默认需要保留这些文件：

```text
configs/default.yaml
models/pretrained/                 # 初始预训练模型
outputs/checkpoints/best/          # 训练后的最佳分类 checkpoint
├── config.json
├── model.safetensors              # 或 pytorch_model.bin，二者至少一个
├── tokenizer.json / vocab.* 等
data/train.csv                     # 相似案例检索数据
data/val.csv                       # 可选，批量评测数据
```

如需切换权重目录，修改 `paths.checkpoint_dir`，并保证其中存在名称以 `best` 开头且包含 `config.json` 与权重文件的 checkpoint 子目录。批量评测只调用分类器，不执行相似案例检索和大模型解释；`data/val.csv` 约 401 条样本，GPU 通常为秒级，CPU 通常为数十秒量级，实际耗时以接口返回的 `elapsed_ms` 为准。

WebUI 和脚本评测共同关注分类指标与解释质量：分类指标包括 Accuracy、Precision、Recall、F1、按 `event` 的错误分析和推理耗时；解释质量关注解释是否与预测标签一致、是否引用输入文本证据、是否区分模型证据/相似案例/事实结论，并避免无依据扩写。

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
│   ├── core/
│   │   ├── batch.py                  # 批量 CSV 分类、指标和混淆矩阵核心逻辑
│   │   └── llm.py                    # 解释模型配置路径、模型列表获取和连接测试核心工具
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
│   ├── cli/
│   │   ├── train.py                 # 训练命令行入口
│   │   ├── evaluate.py              # val.csv 与事件维度评测命令行入口
│   │   └── predict.py               # 单条文本预测命令行入口
│   └── webui/
│       ├── main.py                # 一次启动后端服务和前端界面
│       ├── backend/
│       │   ├── routes.py          # /health、/predict、/explain、/batch、/llm/* 与静态资源
│       │   ├── services/          # 后端服务目录，按接口职责拆分业务逻辑
│       │   │   ├── __init__.py    # 汇总服务接口，供 routes.py 统一调用
│       │   │   ├── health.py      # 服务状态与模型可用性检查
│       │   │   ├── prediction.py  # 单条检测与解释请求适配
│       │   │   ├── batch.py       # 批量评测请求适配，复用 src.core.batch
│       │   │   └── llm.py         # 大模型配置接口适配，复用 src.core.llm
│       │   ├── state.py           # 服务启动时加载并缓存 pipeline
│       │   └── errors.py          # 统一异常类型
│       └── frontend/
│           ├── index.html          # SPA 外壳
│           ├── app.js              # 启动器：主题、组件加载、路由、事件总线
│           ├── core/               # api/bus/health/icons/theme 与 base/theme 样式
│           ├── components/
│           │   ├── single/         # 单条输入、结果、依据、案例和导出步骤
│           │   ├── batch/          # 批量上传、指标、图表、明细和报告步骤
│           │   ├── stepper/        # 两条工作流共用的竖向步进器
│           │   ├── state-card/     # 空态、加载态和错误态卡片
│           │   ├── config/         # 大模型配置与主题化下拉框
│           │   └── status/         # 服务状态监控面板
│           └── resources/          # favicon 与 currentColor SVG 图标等静态资源
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
- CLI 与 WebUI 是两个独立的接口层，不应互相导入业务逻辑；可复用逻辑接口放在 `src/core/` 或已有共享模块中，再由两个接口层分别适配；
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
python -m src.cli.train --config configs/default.yaml

# 在 val.csv 上评测
python -m src.cli.evaluate --config configs/default.yaml --split val

# 单条文本预测
python -m src.cli.predict --text "input tweet here"

# 解释模型配置
# CLI 与 WebUI 共用 configs/explain_llm.local.yaml；旧版 configs/webui_llm.local.yaml 仅作为兼容读取 fallback。

# 启动 WebUI
python -m src.webui.main
```
