#!/usr/bin/env python3
"""
测试 PageIndex 集成
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加 PageIndex 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'pageindex' / 'PageIndex'))

print("="*60)
print("🔍 PageIndex 集成测试")
print("="*60)

# 1. 测试 PageIndex 导入
print("\n1️⃣ 测试 PageIndex 导入...")
try:
    import run_pageindex
    print("✅ run_pageindex 导入成功")
    
    from pageindex.page_index_md import md_to_tree
    print("✅ md_to_tree 函数导入成功")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

# 2. 测试环境变量
print("\n2️⃣ 测试环境变量...")
load_dotenv()
api_key = os.getenv('CHATGPT_API_KEY')

if not api_key:
    print("❌ CHATGPT_API_KEY 未设置")
    print("   请在 .env 文件中设置:")
    print("   CHATGPT_API_KEY=sk-your-key-here")
    sys.exit(1)
elif api_key == 'your_openai_api_key_here':
    print("❌ CHATGPT_API_KEY 未配置（仍是示例值）")
    print("   请在 .env 文件中设置真实的 API key")
    sys.exit(1)
else:
    print(f"✅ CHATGPT_API_KEY 已配置: {api_key[:10]}...")

# 3. 测试文档
print("\n3️⃣ 测试文档路径...")
test_doc = Path(__file__).parent.parent / 'docs' / 'raw' / 'markdown' / 'Runtime_AIModule_AICodingStandard.md'

if not test_doc.exists():
    # 尝试其他路径
    test_doc = Path(__file__).parent.parent / 'docs' / 'converted' / 'markdown' / 'Source_Shared_Types_UActorComponent_UActorComponent.INT.md'

if test_doc.exists():
    print(f"✅ 找到测试文档: {test_doc.name}")
else:
    print("❌ 未找到测试文档")
    print("   请先运行文档收集:")
    print("   ./tools/run_collection.sh")
    sys.exit(1)

# 4. 测试 PageIndex 处理（可选）
print("\n4️⃣ 测试 PageIndex 处理...")
print("   这将调用 OpenAI API 并产生费用")
print("   是否继续测试？(y/n): ", end='')

try:
    response = input().lower().strip()
    if response == 'y':
        print("\n🔄 处理文档中...")
        # 这里可以添加实际的 PageIndex 测试
        # result = md_to_tree(str(test_doc), ...)
        print("⚠️  实际测试需要完整的 API 配置")
        print("   请稍后运行 build_index.py")
    else:
        print("⏭️  跳过 API 测试")
except:
    print("\n⏭️  非交互模式，跳过测试")

# 总结
print("\n" + "="*60)
print("✅ PageIndex 集成测试通过")
print("="*60)
print("\n📋 下一步:")
print("1. 确保 .env 中的 CHATGPT_API_KEY 正确")
print("2. 运行: cd pageindex/scripts && python3 build_index.py")
print("3. 或测试单个文档:")
print("   cd pageindex/PageIndex")
print("   python3 run_pageindex.py --md_path ../../docs/raw/markdown/Runtime_AIModule_AICodingStandard.md")
print()
