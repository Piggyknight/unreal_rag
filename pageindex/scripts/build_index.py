#!/usr/bin/env python3
"""
使用 PageIndex 构建 UE 文档索引
支持 Markdown 文件的批量索引构建
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict
import yaml
from dotenv import load_dotenv

# 添加 PageIndex 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'PageIndex'))

# 检查 PageIndex 是否可用
try:
    # PageIndex 使用 run_pageindex.py 的 process_markdown 函数
    import run_pageindex
    PAGEINDEX_AVAILABLE = True
    print("✅ PageIndex 已加载")
except ImportError as e:
    print(f"⚠️  PageIndex 导入失败: {e}")
    print("   请确保 PageIndex 已正确安装")
    PAGEINDEX_AVAILABLE = False


class PageIndexBuilder:
    """使用 PageIndex 构建 UE 文档索引"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.stats = {
            'total_docs': 0,
            'indexed': 0,
            'failed': 0,
            'errors': []
        }
        
        # 加载环境变量
        load_dotenv()
        
        # 检查 API key (支持 ZAI_API_KEY 或 CHATGPT_API_KEY)
        api_key = os.getenv('ZAI_API_KEY') or os.getenv('CHATGPT_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            raise ValueError(
                "❌ 未配置 API Key\n"
                "请编辑 .env 文件并添加您的 API key:\n"
                "  ZAI_API_KEY=your-glm-key-here\n"
                "  或\n"
                "  CHATGPT_API_KEY=sk-your-key-here"
            )
        
        # 判断使用的API类型
        api_type = "GLM" if os.getenv('ZAI_API_KEY') else "OpenAI"
        print(f"✅ API Key 已配置 ({api_type}): {api_key[:10]}...")
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def find_markdown_files(self, docs_dir: str) -> List[str]:
        """查找所有 Markdown 文件"""
        md_files = []
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))
        return md_files
    
    def build_index_for_doc(
        self,
        doc_path: str,
        output_dir: str,
        category: str = None
    ) -> bool:
        """
        为单个文档构建 PageIndex
        
        Args:
            doc_path: Markdown 文件路径
            output_dir: 输出目录
            category: 可选的分类名称
        
        Returns:
            成功返回 True，失败返回 False
        """
        try:
            # 生成输出文件名
            doc_name = Path(doc_path).stem
            if category:
                output_file = os.path.join(output_dir, category, f"{doc_name}.json")
            else:
                output_file = os.path.join(output_dir, f"{doc_name}.json")
            
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            print(f"  📄 处理: {doc_name}")
            
            # 调用 PageIndex 的 md_to_tree 函数
            import asyncio
            
            # 获取配置参数
            pageindex_config = self.config.get('pageindex', {})
            model = pageindex_config.get('model', 'glm-4-flash')
            
            print(f"  📄 处理: {doc_name} (模型: {model})")
            
            # 调用 md_to_tree
            result = asyncio.run(run_pageindex.md_to_tree(
                md_path=doc_path,
                model=model,
                if_thinning=False,
                if_add_node_summary=pageindex_config.get('add_node_summary', True),
                if_add_doc_description=pageindex_config.get('add_doc_description', True),
                if_add_node_text=False,
                if_add_node_id=pageindex_config.get('add_node_id', True)
            ))
            
            # 保存索引
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"     ✅ 已保存: {output_file}")
            return True
            
        except Exception as e:
            error_msg = f"{doc_path}: {str(e)}"
            self.stats['errors'].append(error_msg)
            print(f"     ❌ 失败: {str(e)}")
            return False
    
    def build_all_indexes(
        self,
        docs_dir: str,
        output_dir: str,
        categorize: bool = True,
        limit: int = None
    ):
        """
        为所有文档构建 PageIndex
        
        Args:
            docs_dir: Markdown 文件目录
            output_dir: 输出目录
            categorize: 是否按类别组织
            limit: 限制处理的文档数量（用于测试）
        """
        print(f"\n🔍 扫描文档目录: {docs_dir}")
        md_files = self.find_markdown_files(docs_dir)
        self.stats['total_docs'] = len(md_files)
        
        print(f"📄 找到 {len(md_files)} 个文档\n")
        
        if limit:
            md_files = md_files[:limit]
            print(f"⚠️  测试模式：仅处理前 {limit} 个文档\n")
        
        if categorize:
            # 按类别分类文档
            categories = self.config.get('categorization', {})
            
            for category, keywords in categories.items():
                print(f"\n📚 处理分类: {category}")
                category_dir = os.path.join(output_dir, category)
                os.makedirs(category_dir, exist_ok=True)
                
                # 查找匹配的文档
                matched_files = []
                for md_file in md_files:
                    file_lower = md_file.lower()
                    if any(keyword.lower() in file_lower for keyword in keywords):
                        matched_files.append(md_file)
                
                print(f"   找到 {len(matched_files)} 个匹配文档")
                
                # 构建索引
                for md_file in matched_files:
                    if self.build_index_for_doc(md_file, category_dir, category):
                        self.stats['indexed'] += 1
                    else:
                        self.stats['failed'] += 1
        else:
            # 不分类，处理所有文档
            for md_file in md_files:
                if self.build_index_for_doc(md_file, output_dir):
                    self.stats['indexed'] += 1
                else:
                    self.stats['failed'] += 1
        
        self._print_summary()
        
        if categorize:
            self._generate_combined_index(output_dir)
    
    def _generate_combined_index(self, output_dir: str):
        """生成组合索引文件"""
        print("\n🔄 生成组合索引...")
        
        combined_index = {
            'version': '1.0',
            'total_documents': self.stats['indexed'],
            'categories': {}
        }
        
        # 扫描所有生成的索引
        for category_dir in Path(output_dir).iterdir():
            if category_dir.is_dir():
                category_name = category_dir.name
                combined_index['categories'][category_name] = []
                
                for index_file in category_dir.glob('*.json'):
                    combined_index['categories'][category_name].append(
                        str(index_file.relative_to(output_dir))
                    )
        
        # 保存组合索引
        combined_file = os.path.join(output_dir, 'combined_index.json')
        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump(combined_index, f, indent=2)
        
        print(f"✅ 组合索引已保存: {combined_file}")
    
    def _print_summary(self):
        """打印构建摘要"""
        print("\n" + "="*60)
        print("📊 PageIndex 构建摘要")
        print("="*60)
        print(f"总文档数:       {self.stats['total_docs']}")
        print(f"已索引:         {self.stats['indexed']}")
        print(f"失败:           {self.stats['failed']}")
        
        if self.stats['errors']:
            print(f"\n❌ 错误 ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:5]:
                print(f"  - {error}")
            if len(self.stats['errors']) > 5:
                print(f"  ... 还有 {len(self.stats['errors'])-5} 个错误")
        
        print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='使用 PageIndex 构建 UE 文档索引'
    )
    parser.add_argument(
        '--config',
        default='../../config/settings.yaml',
        help='配置文件路径'
    )
    parser.add_argument(
        '--docs-dir',
        default='../../docs/converted/markdown',
        help='Markdown 文件目录'
    )
    parser.add_argument(
        '--output',
        default='../generated_indexes',
        help='索引输出目录'
    )
    parser.add_argument(
        '--no-categorize',
        action='store_true',
        help='禁用文档分类'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='限制处理的文档数量（测试用）'
    )
    
    args = parser.parse_args()
    
    if not PAGEINDEX_AVAILABLE:
        print("❌ PageIndex 不可用，无法继续")
        sys.exit(1)
    
    builder = PageIndexBuilder(args.config)
    builder.build_all_indexes(
        args.docs_dir,
        args.output,
        categorize=not args.no_categorize,
        limit=args.limit
    )


if __name__ == '__main__':
    main()
