#!/bin/bash
# 简化的RAG查询工具 - 不依赖PageIndex
# 使用基本的全文搜索作为临时方案

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple
import argparse


class SimpleRAGClient:
    """简化的RAG客户端 - 使用全文搜索"""
    
    def __init__(self, docs_dir: str = None):
        self.docs_dir = os.path.expanduser(docs_dir or '~/Documents/unreal_rag/docs/converted/markdown')
        self.index = {}
        self._build_index()
    
    def _build_index(self):
        """构建简单的文档索引"""
        print(f"📂 扫描文档目录: {self.docs_dir}")
        
        if not os.path.exists(self.docs_dir):
            print(f"❌ 目录不存在: {self.docs_dir}")
            return
        
        md_files = list(Path(self.docs_dir).rglob('*.md'))
        print(f"✅ 找到 {len(md_files)} 个文档\n")
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    self.index[str(md_file)] = {
                        'content': content,
                        'path': str(md_file),
                        'name': md_file.name
                    }
            except Exception as e:
                print(f"⚠️  无法读取 {md_file.name}: {e}")
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        搜索文档
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
        
        Returns:
            匹配的文档列表
        """
        query_lower = query.lower()
        results = []
        
        for doc_path, doc_data in self.index.items():
            content = doc_data['content']
            
            # 计算相关性分数（简单的关键词匹配）
            score = 0
            query_terms = query_lower.split()
            
            for term in query_terms:
                # 统计词频
                count = content.count(term)
                if count > 0:
                    score += count
            
            if score > 0:
                # 提取相关段落
                snippets = self._extract_snippets(content, query_terms)
                
                results.append({
                    'path': doc_path,
                    'name': doc_data['name'],
                    'score': score,
                    'snippets': snippets
                })
        
        # 按分数排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:max_results]
    
    def _extract_snippets(self, content: str, query_terms: List[str], 
                         context_chars: int = 200) -> List[str]:
        """提取包含查询词的段落"""
        snippets = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(term in line_lower for term in query_terms):
                # 获取上下文（前后各几行）
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                snippet = '\n'.join(lines[start:end])
                snippets.append(snippet)
                
                if len(snippets) >= 3:  # 每个文档最多3个片段
                    break
        
        return snippets
    
    def interactive_query(self):
        """交互式查询模式"""
        print("\n" + "="*60)
        print("🔍 UE文档查询系统（简化版）")
        print("="*60)
        print(f"📚 已索引 {len(self.index)} 个文档")
        print("💡 输入 'quit' 或 'exit' 退出\n")
        
        while True:
            try:
                query = input("🔎 请输入查询: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 再见!")
                    break
                
                if not query:
                    continue
                
                print(f"\n🔍 搜索: {query}...")
                results = self.search(query, max_results=5)
                
                if not results:
                    print("❌ 未找到相关文档\n")
                    continue
                
                print(f"\n✅ 找到 {len(results)} 个相关文档:\n")
                
                for i, result in enumerate(results, 1):
                    print(f"\n{i}. {result['name']} (相关度: {result['score']})")
                    print(f"   📄 {result['path']}")
                    print("\n   摘要:")
                    for j, snippet in enumerate(result['snippets'][:1], 1):
                        # 清理并格式化snippet
                        clean_snippet = snippet.strip()[:300]
                        print(f"   {clean_snippet}...")
                    print("-" * 60)
                
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 再见!")
                break
            except Exception as e:
                print(f"❌ 错误: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description='简化版UE文档查询工具'
    )
    parser.add_argument(
        '--docs-dir',
        default='~/Documents/unreal_rag/docs/converted/markdown',
        help='文档目录路径'
    )
    parser.add_argument(
        '--query',
        help='查询内容（如不提供则进入交互模式）'
    )
    parser.add_argument(
        '--max-results',
        type=int,
        default=5,
        help='最大结果数'
    )
    
    args = parser.parse_args()
    
    client = SimpleRAGClient(args.docs_dir)
    
    if args.query:
        # 单次查询模式
        results = client.search(args.query, args.max_results)
        print(f"\n搜索结果: {args.query}\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['name']} (分数: {result['score']})")
            print(f"   {result['path']}\n")
    else:
        # 交互模式
        client.interactive_query()


if __name__ == '__main__':
    main()
