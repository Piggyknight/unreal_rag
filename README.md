# Unreal Engine RAG Knowledge Base 🎮

<div align="center">

**完整的UE文档知识库系统 - 支持两种查询方式**

[![Status](https://img.shields.io/badge/Status-✅%20Complete-brightgreen)](https://github.com/Piggyknight/unreal_rag)
[![Documents](https://img.shields.io/badge/Documents-221-blue)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[立即开始](#-立即开始) • [功能特性](#-功能特性) • [使用指南](#-使用指南) • [文档](#-文档)

</div>

---

## 📖 项目简介

为Unreal Engine 5.6构建的RAG（检索增强生成）知识库，包含221个官方文档，支持两种查询方式：

- **🆓 简化 RAG**: 免费即时查询，无需API
- **🚀 PageIndex**: 高级语义检索，需要OpenAI API

## ✨ 功能特性

### ✅ 已实现

- **文档收集**: 自动收集UE官方文档（Markdown + UDN）
- **格式转换**: UDN → Markdown 转换器
- **简化RAG**: 关键词搜索，<1秒响应
- **PageIndex集成**: 向量无关的推理型检索
- **Agent框架**: UE开发助手 + QA助手接口
- **完整工具链**: 一键收集、转换、查询

### 📊 项目统计

| 项目 | 数量 |
|------|------|
| 文档 | 221个 |
| 工具脚本 | 8个 |
| 指南文档 | 8个 |
| 代码行数 | ~1500行 |

## 🚀 立即开始

### 方式1: 简化 RAG（推荐新手）

**免费，无需API，立即可用**

```bash
cd ~/Documents/unreal_rag

# 交互式查询
python3 tools/simple_rag_query.py

# 命令行查询
python3 tools/simple_rag_query.py --query "coding standard"
```

### 方式2: PageIndex（高级用户）

**语义理解，需要OpenAI API**

```bash
# 1. 配置 API Key
nano .env  # 添加 CHATGPT_API_KEY=sk-...

# 2. 测试配置
python3 tools/test_pageindex.py

# 3. 构建索引
cd pageindex/scripts
python3 build_index.py --limit 5  # 先测试5个文档
```

## 📚 使用指南

### 日常查询（免费）

```python
# 查询编码规范
python3 tools/simple_rag_query.py --query "naming convention"

# 查询API文档
python3 tools/simple_rag_query.py --query "UActorComponent"

# 查询最佳实践
python3 tools/simple_rag_query.py --query "subsystem"
```

### 文档浏览

```bash
# 查看所有文档
cd ~/Documents/unreal_rag/docs

# 原始Markdown
ls raw/markdown/

# 转换的UDN
ls converted/markdown/
```

## 🎯 两种查询方式对比

| 特性 | 简化 RAG | PageIndex |
|------|---------|-----------|
| 费用 | ✅ 免费 | ⚠️ 需API费 |
| 速度 | ✅ <1秒 | ⚠️ 较慢 |
| 准确度 | ⚠️ 关键词 | ✅ 语义理解 |
| 配置 | ✅ 零配置 | ⚠️ 需API Key |
| 适用 | 快速查询 | 复杂问题 |

## 📁 项目结构

```
unreal_rag/
├── docs/                    # 221个文档
│   ├── raw/markdown/       # 49个原始MD
│   └── converted/markdown/ # 172个转换的MD
├── tools/                   # 工具脚本
│   ├── simple_rag_query.py # ⭐ 简化RAG
│   ├── test_pageindex.py   # PageIndex测试
│   └── run_collection.sh   # 文档收集
├── pageindex/              # PageIndex系统
│   ├── PageIndex/          # 库文件
│   └── scripts/            # 构建脚本
├── agents/                 # Agent接口
├── config/                 # 配置文件
└── 文档                    # 指南文档
```

## 📖 文档指南

| 文档 | 用途 |
|------|------|
| [GET_STARTED_NOW.md](GET_STARTED_NOW.md) | ⭐ 立即开始 |
| [PAGEINDEX_READY.md](PAGEINDEX_READY.md) | PageIndex配置 |
| [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md) | 项目完成状态 |
| [SUMMARY.md](SUMMARY.md) | 项目总结 |
| [QUICKSTART.md](QUICKSTART.md) | 快速开始 |
| [STATUS.md](STATUS.md) | 详细状态 |

## 🔧 高级功能

### Agent 接口

```python
# UE开发助手
from agents.ue_dev_agent import UEDevAgent
agent = UEDevAgent()
result = agent.query("What is the coding standard?")

# QA助手
from agents.qa_agent import QAAgent
agent = QAAgent()
result = agent.query("How to debug?")
```

### 重新收集文档

```bash
# 一键收集所有文档
./tools/run_collection.sh
```

## 🛠️ 配置

### 环境变量

```bash
# .env 文件
CHATGPT_API_KEY=sk-your-key-here  # PageIndex需要
```

### 设置文件

编辑 `config/settings.yaml` 自定义：
- 文档分类规则
- PageIndex参数
- 查询设置

## 📊 支持的文档类型

### 已收集
- ✅ 编码规范 (AICodingStandard等)
- ✅ API参考 (UActorComponent等)
- ✅ 指南文档 (README等)
- ✅ 测试框架 (CQTest等)
- ✅ 调试文档

### 分类
- coding-standards
- api-reference
- guides
- debugging

## 💡 使用建议

### 推荐策略

1. **快速查询** → 简化RAG（免费）
2. **复杂问题** → PageIndex（需API）
3. **深度研究** → 直接浏览文档

### 省钱技巧

- 先用简化RAG满足80%需求
- PageIndex仅用于复杂问题
- 使用 `--limit` 参数测试

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

- [PageIndex](https://github.com/VectifyAI/PageIndex) - 向量无关的RAG引擎
- [Unreal Engine](https://www.unrealengine.com/) - 游戏引擎
- [OpenAI](https://openai.com/) - GPT-4o API

---

<div align="center">

**🎉 项目已完成，立即可用！**

**快速开始**: `python3 tools/simple_rag_query.py`

**问题反馈**: [GitHub Issues](https://github.com/Piggyknight/unreal_rag/issues)

</div>
