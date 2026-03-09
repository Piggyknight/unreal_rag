# UE RAG Project - Phase 2: PageIndex Setup Script
# This script completes PageIndex integration

#!/bin/bash

set -e

PROJECT_ROOT=~/Documents/unreal_rag
cd $PROJECT_ROOT/pageindex

echo "=================================================="
echo "🔄 PageIndex Setup Script"
echo "=================================================="
echo ""

# Check if PageIndex.zip was downloaded
if [ -f "PageIndex.zip" ]; then
    echo "✅ Found PageIndex.zip"
    echo "📦 Extracting..."
    unzip -q PageIndex.zip
    mv PageIndex-main PageIndex
    rm PageIndex.zip
    echo "✅ Extracted successfully"
else
    echo "❌ PageIndex.zip not found"
    echo "   Trying to clone with git..."
    git clone https://github.com/VectifyAI/PageIndex.git || {
        echo "❌ Git clone failed"
        echo "   Please manually download from:"
        echo "   https://github.com/VectifyAI/PageIndex/archive/refs/heads/main.zip"
        exit 1
    }
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
cd PageIndex
pip3 install -r requirements.txt --user -q

echo "✅ Dependencies installed"

# Check for API key
cd $PROJECT_ROOT
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found"
    echo "   Creating from template..."
    cp .env.example .env
    echo ""
    echo "🔴 IMPORTANT: Edit .env and add your OpenAI API key:"
    echo "   nano .env"
    echo "   Add: CHATGPT_API_KEY=sk-your-key-here"
    echo ""
else
    if grep -q "your_openai_api_key_here" .env; then
        echo ""
        echo "⚠️  .env exists but API key not set"
        echo "   Please edit .env and add your CHATGPT_API_KEY"
        echo ""
    else
        echo "✅ .env configured"
    fi
fi

# Build indexes
echo ""
echo "=================================================="
echo "📊 Ready to build indexes!"
echo "=================================================="
echo ""
echo "Run this command to build PageIndex for all documents:"
echo ""
echo "  cd ~/Documents/unreal_rag/pageindex/scripts"
echo "  python3 build_index.py"
echo ""
echo "This will process 221 documents and create the RAG knowledge base."
echo ""
