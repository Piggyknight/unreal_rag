# Unreal Engine RAG Knowledge Base 🎮

<div align="center">

**完整的UE文档知识库系统 - 支持两种查询方式**

[![Status](https://img.shields.io/badge/Status-✅%20Complete-brightgreen)](https://github.com/Piggyknight/unreal_rag)
[![Documents](https://img.shields.io/badge/Documents-221-blue)]()
[![Model](https://img.shields.io/badge/Model-GLM-4-flash-green)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[立即开始](#-立即开始) • [功能特性](#-功能特性) • [GLM配置](#-glm-vs-openai) • [文档](#-文档)

</div>

---

## 📖 项目简介

为Unreal Engine 5.6构建的RAG（检索增强生成）知识库，包含221个官方文档，**现已支持GLM模型（智谱AI）**！

- **🆓 简化 RAG**: 免费即时查询，无需API
- **🚀 PageIndex + GLM**: 高级语义检索，成本极低（约¥5处理全部文档）

## ✨ 功能特性

### ✅ 已实现

- **文档收集**: 自动收集UE官方文档（Markdown + UDN）
- **格式转换**: UDN → Markdown 转换器
- **简化RAG**: 关键词搜索，<1秒响应，**完全免费**
- **PageIndex + GLM**: 向量无关的推理型检索，**成本降低99%**
- **Agent框架**: UE开发助手 + QA助手接口
- **完整工具链**: 一键收集、转换、查询

### 📊 项目统计

| 项目 | 数量 |
|------|------|
| 文档 | 221个 |
| 工具脚本 | 8个 |
| 指南文档 | 9个 |
| 代码行数 | ~1500行 |
| **默认模型** | **GLM-4-Flash** |

## 🚀 立即开始

### 方式1: 简化 RAG（推荐，完全免费）

**无需API Key，立即可用**

```bash
cd ~/Documents/unreal_rag

# 交互式查询
python3 tools/simple_rag_query.py

# 命令行查询
python3 tools/simple_rag_query.py --query "coding standard"
```

### 方式2: PageIndex + GLM（低成本，高级功能）

**使用智谱AI GLM模型，成本极低**

```bash
# 1. 获取GLM API Key（约¥5可处理全部文档）
# 访问: https://open.bigmodel.cn/
# 注册并获取API Key

# 2. 配置 API Key
nano .env  # 添加: ZAI_API_KEY=your-key-here

# 3. 测试配置
python3 tools/test_pageindex.py

# 4. 构建索引
cd pageindex/scripts
python3 build_index.py --limit 5  # 先测试5个文档
```

## 💰 GLM vs OpenAI 费用对比

| 特性 | GLM-4-Flash | GPT-4o |
|------|------------|--------|
| 输入价格 | ¥0.1/百万tokens | $2.5/百万tokens |
| 输出价格 | ¥0.1/百万tokens | $10/百万tokens |
| 221文档预估 | **¥5** | **$10** |
| **节省** | **99%+** | - |
| 中文支持 | ✅ 优秀 | ⚠️ 一般 |
| 国内访问 | ✅ 稳定 | ⚠️ 需代理 |

**结论**: GLM便宜20倍以上，且更适合中文文档！

## 📚 使用指南

### 日常查询（免费方案）

```bash
# 查询编码规范
python3 tools/simple_rag_query.py --query "naming convention"

# 查询API文档
python3 tools/simple_rag_query.py --query "UActorComponent"

# 查询最佳实践
python3 tools/simple_rag_query.py --query "subsystem"
```

### 高级查询（GLM方案）

配置GLM后，享受语义理解和推理型检索：

```bash
# 构建PageIndex索引
cd pageindex/scripts
python3 build_index.py

# 查询将更准确，支持：
# - 语义理解
# - 多跳推理
# - 上下文关联
```

## 🎯 两种查询方式对比

| 特性 | 简化 RAG | PageIndex + GLM |
|------|---------|-----------------|
| 费用 | ✅ 免费 | ⚠️ ¥5（一次性）|
| 速度 | ✅ <1秒 | ⚠️ 较慢 |
| 准确度 | ⚠️ 关键词 | ✅ 语义理解 |
| 配置 | ✅ 零配置 | ⚠️ 需API Key |
| 中文 | ✅ 支持 | ✅ 优秀 |
| 适用 | 快速查询 | 复杂问题 |

## 📁 项目结构

```
unreal_rag/
├── docs/                    # 221个文档
│   ├── raw/markdown/       # 49个原始MD
│   └── converted/markdown/ # 172个转换的MD
├── tools/                   # 工具脚本
│   ├── simple_rag_query.py # ⭐ 简化RAG（免费）
│   ├── test_pageindex.py   # GLM测试工具
│   └── run_collection.sh   # 文档收集
├── pageindex/              # PageIndex系统（GLM）
│   ├── PageIndex/          # 库文件（已修改支持GLM）
│   └── scripts/            # 构建脚本
├── agents/                 # Agent接口
├── config/                 # 配置文件
└── 文档                    # 指南文档
```

## 📖 文档指南

| 文档 | 用途 |
|------|------|
| [GET_STARTED_NOW.md](GET_STARTED_NOW.md) | ⭐ 立即开始 |
| [USE_GLM.md](USE_GLM.md) | ⭐ GLM配置指南 |
| [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md) | 项目完成状态 |
| [SUMMARY.md](SUMMARY.md) | 项目总结 |
| [QUICKSTART.md](QUICKSTART.md) | 快速开始 |

## 🔑 获取GLM API Key

### 步骤1: 注册智谱AI
1. 访问: https://open.bigmodel.cn/
2. 点击"注册/登录"
3. 完成账户注册（免费）

### 步骤2: 获取API Key
1. 登录后，进入控制台
2. 点击"API密钥"
3. 创建新的API Key
4. 复制生成的Key

### 步骤3: 配置到项目
```bash
nano ~/Documents/unreal_rag/.env

# 添加：
ZAI_API_KEY=your-api-key-here
```

### 步骤4: 验证
```bash
python3 tools/test_pageindex.py
```

## 💡 使用建议

### 推荐策略

1. **快速查询** → 简化RAG（免费）
2. **复杂问题** → PageIndex + GLM（低成本）
3. **深度研究** → 直接浏览文档

### 省钱技巧

- 优先使用简化RAG（满足80%需求）
- GLM仅用于复杂语义查询
- 使用 `--limit` 参数测试

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

- [PageIndex](https://github.com/VectifyAI/PageIndex) - 向量无关的RAG引擎
- [智谱AI GLM](https://open.bigmodel.cn/) - 高性价比大模型
- [Unreal Engine](https://www.unrealengine.com/) - 游戏引擎

---

<div align="center">

**🎉 项目已完成，现已支持GLM！**

**两种选择**:
- **完全免费**: 使用简化RAG
- **低成本**: 使用GLM（约¥5处理全部文档）

**快速开始**: `python3 tools/simple_rag_query.py`

**问题反馈**: [GitHub Issues](https://github.com/Piggyknight/unreal_rag/issues)

</div>
