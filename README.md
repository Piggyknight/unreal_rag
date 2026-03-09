# Unreal Engine RAG Knowledge Base

Build a vectorless RAG knowledge base from Unreal Engine documentation using PageIndex for UE development agents and QA agents.

## 🎯 Purpose

This project provides tools to:
- Collect UE documentation from `.md` and `.udn` files
- Convert UDN format to standard Markdown
- Generate PageIndex tree structures for reasoning-based RAG
- Query the knowledge base for development and debugging assistance

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ~/Documents/unreal_rag
pip3 install -r requirements.txt
```

### 2. Configure Settings

Edit `config/settings.yaml` to set your Unreal Engine paths:

```yaml
unreal_engine:
  engine_path: ~/Documents/ue_56/Engine
  source_path: ~/Documents/ue_56/Engine/Source
  docs_path: ~/Documents/ue_56/Engine/Documentation
```

### 3. Run Collection Pipeline

```bash
# Collect and convert all documentation
./tools/run_collection.sh
```

This will:
- Collect all `.md` files from `Engine/Source`
- Collect all `.udn` files from `Engine/Documentation` 
- Convert UDN files to Markdown format
- Generate collection reports

### 4. Set Up PageIndex

```bash
# Clone PageIndex as submodule
cd ~/Documents/unreal_rag
git submodule add https://github.com/VectifyAI/PageIndex.git pageindex/PageIndex

# Configure OpenAI API key
echo "CHATGPT_API_KEY=your_key_here" > .env
```

### 5. Build RAG Index

```bash
# Generate PageIndex for all documents
python3 pageindex/scripts/build_index.py
```

## 📁 Project Structure

```
unreal_rag/
├── docs/                    # Collected documentation
│   ├── raw/                # Original files
│   │   ├── markdown/       # .md files from Source
│   │   └── udn/            # .udn files from Documentation
│   ├── converted/          # Converted to standard format
│   │   └── markdown/       # All docs in markdown
│   └── categorized/        # Organized by category
│       ├── coding-standards/
│       ├── api-reference/
│       ├── guides/
│       └── debugging/
├── tools/                   # Processing scripts
│   ├── collectors/         # Document collection
│   ├── converters/         # Format conversion
│   ├── organizers/         # Categorization
│   └── run_collection.sh   # Main pipeline script
├── pageindex/              # PageIndex integration
│   ├── PageIndex/          # Git submodule
│   ├── generated_indexes/  # Tree structures
│   └── scripts/            # Build and query scripts
├── agents/                 # Agent interfaces
│   ├── ue_dev_agent.py
│   ├── qa_agent.py
│   └── shared/rag_client.py
└── config/                 # Configuration
    └── settings.yaml
```

## 🔧 Individual Tools

### Collect Markdown Files

```bash
python3 tools/collectors/collect_markdown.py \
    --config config/settings.yaml \
    --output docs/raw/markdown
```

### Collect UDN Files

```bash
# Collect all languages
python3 tools/collectors/collect_udn.py \
    --output docs/raw/udn

# Collect specific languages only
python3 tools/collectors/collect_udn.py \
    --output docs/raw/udn \
    --languages INT CHN
```

### Convert UDN to Markdown

```bash
python3 tools/converters/udn_to_markdown.py \
    --input docs/raw/udn \
    --output docs/converted/markdown \
    --languages INT
```

## 🤖 Using with Agents

### UE Dev Agent

```python
from agents.ue_dev_agent import UEDevAgent

agent = UEDevAgent()
result = agent.query("What is the coding standard for naming variables?")
print(result)
```

### QA Agent

```python
from agents.qa_agent import QAAgent

agent = QAAgent()
result = agent.query("How do I debug a null pointer in UE?")
print(result)
```

## 📊 Expected Results

After running the collection pipeline, you should have:
- **~70 markdown files** from Engine/Source
- **~600+ UDN files** (673 total, with language variants)
- **~600+ converted markdown files** from UDN

## 🛠️ PageIndex Integration

PageIndex provides vectorless, reasoning-based retrieval:

1. **No Vector DB**: Uses document structure and LLM reasoning
2. **No Chunking**: Preserves natural document sections
3. **Human-like Retrieval**: Simulates expert document navigation

## 🔍 Example Queries

- "What are the naming conventions for UE classes?"
- "How do I use the TArray container?"
- "What is the coding standard for subsystems?"
- "How to optimize navmesh generation?"

## 📝 Configuration

Key settings in `config/settings.yaml`:

- `unreal_engine.paths`: UE installation paths
- `collection.exclude_patterns`: Files/folders to skip
- `pageindex.model`: OpenAI model for indexing
- `categorization`: Rules for organizing documents
- `query`: RAG retrieval settings

## 🧪 Testing

```bash
# Test document collection
python3 tests/test_collection.py

# Test query functionality
python3 tests/test_query.py
```

## 📖 Documentation

- [Project Plan](PROJECT_PLAN.md)
- [PageIndex Documentation](https://docs.pageindex.ai)
- [PageIndex Framework](https://pageindex.ai/blog/pageindex-intro)

## 🤝 Contributing

This is a personal knowledge base project, but suggestions and improvements are welcome!

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

**Created for**: Unreal Engine 5.6 documentation  
**Powered by**: PageIndex - Vectorless RAG  
**Status**: ✅ Phase 1 Complete (Collection & Conversion)
