#!/bin/bash
# UE Documentation Collection Pipeline
# Runs all collection and conversion steps

set -e  # Exit on error

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "=================================================="
echo "🚀 UE Documentation Collection Pipeline"
echo "=================================================="
echo ""

# Step 1: Collect Markdown files
echo "📋 Step 1: Collecting Markdown files..."
python3 tools/collectors/collect_markdown.py \
    --config config/settings.yaml \
    --output docs/raw/markdown \
    --report docs/markdown_collection_report.yaml

echo ""

# Step 2: Collect UDN files (INT language only by default)
echo "📋 Step 2: Collecting UDN files (English/INT)..."
python3 tools/collectors/collect_udn.py \
    --config config/settings.yaml \
    --output docs/raw/udn \
    --report docs/udn_collection_report.yaml \
    --languages INT

echo ""

# Step 3: Convert UDN to Markdown
echo "🔄 Step 3: Converting UDN to Markdown..."
python3 tools/converters/udn_to_markdown.py \
    --input docs/raw/udn \
    --output docs/converted/markdown \
    --languages INT

echo ""

# Summary
echo "=================================================="
echo "✅ Collection Pipeline Complete!"
echo "=================================================="
echo ""
echo "📊 Summary:"
echo "  - Markdown files: $(ls -1 docs/raw/markdown/*.md 2>/dev/null | wc -l)"
echo "  - UDN files:      $(find docs/raw/udn -name '*.udn' 2>/dev/null | wc -l)"
echo "  - Converted MD:   $(find docs/converted/markdown -name '*.md' 2>/dev/null | wc -l)"
echo ""
echo "📁 Output locations:"
echo "  - Raw Markdown:   docs/raw/markdown/"
echo "  - Raw UDN:        docs/raw/udn/"
echo "  - Converted MD:   docs/converted/markdown/"
echo "  - Reports:        docs/*_collection_report.yaml"
echo ""
