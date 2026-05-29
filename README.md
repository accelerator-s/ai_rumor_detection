# 可解释的谣言检测系统

本项目是《人工智能导论》课程大作业“可解释的谣言检测”的工程实现。目标是在给定推文文本后，输出二分类检测结果，并给出一段可读的判断依据。

分类标签定义如下：

- `0`：非谣言
- `1`：谣言

项目以 `data/train.csv` 作为训练集，以 `data/val.csv` 作为官方验证集。数据字段包括 `id`、`text`、`label`、`event`。

## 设计目标

本项目优先满足以下目标：

1. **控制过拟合风险**：谣言检测容易受到具体事件、人名、地名和话题标签影响。由于训练数据规模有限，模型可能记住训练集中出现过的事件表面特征，因此需要在文本归一化、事件感知验证、正则化训练和错误分析中持续关注过拟合问题。
2. **本地可训练**：训练过程面向普通笔记本电脑独立显卡设计，控制模型规模、序列长度、batch size 和依赖复杂度，保证合理运行时间。
3. **检测与解释分层**：分类模型负责给出标签和概率，解释模块负责把模型证据、相似样本和文本特征组织成自然语言依据。
4. **仓库可复现**：训练、评测、预测和解释流程均通过脚本运行，最终结果以 `val.csv` 上的准确率作为主要检测指标。

## 技术路线

系统采用“深度分类模型 + 轻量检索 + 解释生成”的复合结构。

### 1. 文本预处理与泛化处理

推文文本包含 URL、用户提及、转发标记、话题标签、HTML 转义字符等噪声。预处理模块会进行统一归一化：

- 将 URL、用户提及、转发标记归一为稳定占位符；
- 处理 HTML 转义字符；
- 保留否定词、情绪词、标点和话题标签中的有效语义；
- 构造“原始文本视图”和“泛化文本视图”，减少模型对单一事件实体的依赖。

泛化文本视图不会简单删除所有实体信息，而是对强事件绑定的片段进行规范化。这样既避免模型死记硬背具体事件，也尽量保留谣言检测所需的语义线索。

### 2. 分类模型

主分类模型采用面向英文短文本的预训练语言模型进行二分类微调。优先使用适合推文语料的 BERTweet 类模型；如本地环境受限，则使用 RoBERTa 类模型作为同架构替代。

训练策略包括：

- 最大序列长度控制在短推文适合的范围内；
- 使用较小 batch size、梯度累积和混合精度训练，适配笔记本 GPU；
- 使用验证集监控 early stopping，避免小数据集过拟合；
- 记录 accuracy、precision、recall、F1 和推理耗时；
- 保存最优模型权重和 tokenizer 配置。

为保证实验可信度，项目同时保留一个轻量基线模型，例如 `TF-IDF + Logistic Regression / Linear SVM`。基线模型用于校验数据处理、评测脚本和主模型提升是否真实有效。

### 3. 泛化能力评估

除官方 `val.csv` 评测外，训练阶段会利用 `event` 字段进行事件感知分析。具体做法是按事件划分训练内验证组合，观察模型在不同事件上的表现差异。

该部分用于回答两个问题：

- 模型是否只在高频事件上表现较好；
- 文本归一化、正则化训练和事件泛化处理是否降低了事件记忆风险。

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
2. **自然语言解释生成**：综合预测标签、置信度、重要片段和相似案例，生成一段面向用户的判断依据。

如果使用大语言模型生成解释，将通过 SJTU API 的 OpenAI 兼容接口调用。大语言模型只负责组织表达，不直接决定分类标签。最终解释应围绕可观察证据展开，避免把相似案例描述成外部事实证据。

结构化提示词工程会参考成熟 CLI Agent 项目的上下文组织方式，但它不是本项目的核心评分点。README 中不展开具体 prompt 细节。

## 计划目录结构

当前阶段先确定工程说明，后续实现会按如下结构组织：

```text
.
├── data/
│   ├── train.csv
│   └── val.csv
├── configs/
│   └── default.yaml
├── docs/
├── src/
│   ├── data/
│   │   └── preprocess.py
│   ├── models/
│   │   ├── baseline.py
│   │   └── transformer_classifier.py
│   ├── retrieval/
│   │   └── tfidf_retriever.py
│   ├── explain/
│   │   ├── evidence.py
│   │   └── generator.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
├── outputs/
│   ├── checkpoints/
│   ├── metrics/
│   └── predictions/
├── requirements.txt
├── app.py
├── README.md
└── report.pdf
```

## 代码组织要求

代码实现遵循以下代码组织原则：

- 单个源代码文件不宜过长，原则上不超过 1000 行；
- 文件之间责任清晰，避免把数据处理、模型训练、评测、解释生成和界面逻辑混在同一个文件中；
- 核心模块通过明确接口连接，例如 `Classifier`、`Retriever`、`Explainer`、`Predictor` 等；
- 训练、评测、预测和解释流程应能分别独立运行，也能在端到端入口中组合调用；
- 配置项集中放在 `configs/` 中，避免在多个脚本中散落硬编码参数；
- 对外部模型接口和本地模型推理做封装，避免业务代码直接依赖具体 API 调用细节。

## 运行方式

后续实现完成后，项目将提供以下入口：

建议使用 Python 3.11。项目可以在 CPU 环境下运行，基线模型训练和单条推理不依赖 GPU；若要加速深度分类模型训练，需要使用支持 CUDA 的 NVIDIA GPU，并安装与本机显卡驱动和 CUDA 环境匹配的 PyTorch 版本。

PyTorch 需要根据本机 CPU/CUDA 环境单独安装，不写入通用 `requirements.txt` 中。安装时应在 PyTorch 官网选择当前 Stable 版本，并匹配本机操作系统、Python 版本和计算平台。示例命令如下，实际安装命令以 PyTorch 官网为准：

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

# 训练基线模型
python -m src.train --config configs/default.yaml --model baseline

# 训练深度分类模型
python -m src.train --config configs/default.yaml --model transformer

# 在 val.csv 上评测
python -m src.evaluate --config configs/default.yaml --split val

# 单条文本预测
python -m src.predict --text "input tweet here"

# 启动交互界面
python app.py
```

## 评测指标

分类性能：

- Accuracy：对应作业评分中的 `val.csv` 分类准确率；
- Precision / Recall / F1：用于分析类别不均衡和错误类型；
- Per-event metrics：用于分析事件泛化情况；
- Inference time：用于说明运行时间是否合理。

解释质量：

- 是否与模型预测标签一致；
- 是否引用了输入文本中的具体证据；
- 是否区分“模型证据”“相似案例”和“事实结论”；
- 是否避免无依据扩写。
