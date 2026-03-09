# Quick Start Guide - UE RAG Knowledge Base

## ✅ Current Progress

**Phase 1: Document Collection & Conversion** - COMPLETE

### Collected Documents:
- ✅ **49 Markdown files** from Engine/Source
- ✅ **172 UDN files** (English/INT language)  
- ✅ **172 Converted** UDN → Markdown

### Key Documents Available:
- **Coding Standards**: AICodingStandard.md
- **API Documentation**: UActorComponent, variable types, etc.
- **Test Framework**: Catch2 documentation
- **Developer Tools**: CQTest, LowLevelTestsRunner
- **Engine Modules**: MathCore, NavigationSystem, etc.

## 🔄 Next Steps

### Step 1: Complete PageIndex Setup

```bash
# 1. Navigate to project
cd ~/Documents/unreal_rag

# 2. Clone PageIndex (if not already done)
cd pageindex
git clone https://github.com/VectifyAI/PageIndex.git

# 3. Install PageIndex dependencies
cd PageIndex
pip3 install -r requirements.txt

# 4. Configure OpenAI API key
cd ~/Documents/unreal_rag
cp .env.example .env
# Edit .env and add your CHATGPT_API_KEY
```

### Step 2: Build PageIndex

```bash
# Build indexes for all documents (categorized)
cd ~/Documents/unreal_rag/pageindex/scripts
python3 build_index.py

# Or build without categorization
python3 build_index.py --no-categorize
```

This will:
- Process all 221 documents (49 + 172)
- Generate PageIndex tree structures
- Categorize by: coding-standards, api-reference, guides, debugging
- Create combined index for unified queries

### Step 3: Create Query Interface

```bash
# Create RAG query client for agents
cd ~/Documents/unreal_rag/agents/shared
# (We'll create query_index.py next)
```

## 📊 Expected Output

After building indexes, you'll have:

```
pageindex/generated_indexes/
├── combined_index.json          # Master index
├── coding-standards/            # 1-5 indexes
│   ├── AICodingStandard.json
│   └── ...
├── api-reference/               # 150+ indexes
│   ├── UActorComponent.json
│   ├── VariableTypes.json
│   └── ...
├── guides/                      # 30+ indexes
│   ├── README.json
│   └── ...
└── debugging/                   # 10+ indexes
    ├── TestFramework.json
    └── ...
```

## 🎯 Usage Examples

Once indexes are built:

```python
# Query coding standards
from agents.ue_dev_agent import UEDevAgent

agent = UEDevAgent()
response = agent.query("What is the naming convention for subsystems?")
# Returns: "WorldSubsystem-derived classes need to have a Subsystem postfix..."

# Query API reference
response = agent.query("What is UActorComponent?")
# Returns: "An ActorComponent is a reusable component that can be added to any actor..."
```

## ⚠️ Current Status

- ✅ Documents collected and converted
- ⏳ PageIndex clone in progress (network issues)
- ⏳ Need to set CHATGPT_API_KEY
- ⏳ Build indexes
- ⏳ Create agent interfaces

## 🛠️ Troubleshooting

### If PageIndex clone fails:
```bash
# Try with shallow clone
git clone --depth=1 https://github.com/VectifyAI/PageIndex.git

# Or download ZIP
wget https://github.com/VectifyAI/PageIndex/archive/refs/heads/main.zip
unzip main.zip
mv PageIndex-main PageIndex
```

### If missing dependencies:
```bash
pip3 install openai PyPDF2 pdf2image Pillow python-dotenv pyyaml tqdm colorama
```

## 📝 Configuration

Edit `config/settings.yaml` to customize:
- PageIndex model (default: gpt-4o)
- Document categorization rules
- Query settings (max results, relevance score)
- Agent preferences

---

**Status**: Ready for PageIndex build once network issue resolved  
**Next Action**: Complete PageIndex setup → Build indexes → Test queries
