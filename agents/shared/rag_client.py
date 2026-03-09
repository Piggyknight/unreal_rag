#!/usr/bin/env python3
"""
RAG Query Client - Query interface for UE documentation knowledge base
Used by UE Dev Agent and QA Agent
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
import yaml


class RAGQueryClient:
    """Query client for UE documentation RAG system"""
    
    def __init__(self, index_dir: str = None, config_path: str = None):
        """
        Initialize RAG query client
        
        Args:
            index_dir: Directory containing PageIndex files
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.index_dir = index_dir or os.path.expanduser(
            '~/Documents/unreal_rag/pageindex/generated_indexes'
        )
        self.combined_index = None
        self.category_indexes = {}
        
        self._load_indexes()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_indexes(self):
        """Load combined index and category mappings"""
        combined_path = os.path.join(self.index_dir, 'combined_index.json')
        
        if os.path.exists(combined_path):
            with open(combined_path, 'r') as f:
                self.combined_index = json.load(f)
                print(f"✅ Loaded combined index: {self.combined_index.get('total_documents', 0)} documents")
        else:
            print(f"⚠️  Combined index not found at {combined_path}")
            print("   Please run: python3 pageindex/scripts/build_index.py")
    
    def search(
        self,
        query: str,
        categories: List[str] = None,
        max_results: int = 5,
        min_score: float = 0.7
    ) -> List[Dict]:
        """
        Search documentation for relevant content
        
        Args:
            query: Search query
            categories: Categories to search (None = all)
            max_results: Maximum results to return
            min_score: Minimum relevance score
        
        Returns:
            List of relevant document sections
        """
        if not self.combined_index:
            return []
        
        results = []
        
        # Determine which categories to search
        search_categories = categories or list(self.combined_index.get('categories', {}).keys())
        
        # TODO: Implement actual PageIndex query here
        # For now, return placeholder
        
        print(f"🔍 Searching for: {query}")
        print(f"   Categories: {', '.join(search_categories)}")
        print(f"   Max results: {max_results}")
        
        # Placeholder implementation
        # In production, this would use PageIndex's reasoning-based retrieval
        
        return results
    
    def get_document(self, doc_name: str, category: str = None) -> Optional[Dict]:
        """
        Get specific document by name
        
        Args:
            doc_name: Document name (without .json)
            category: Category to search in (optional)
        
        Returns:
            Document content or None
        """
        if category:
            # Search in specific category
            index_file = os.path.join(
                self.index_dir,
                category,
                f"{doc_name}.json"
            )
            if os.path.exists(index_file):
                with open(index_file, 'r') as f:
                    return json.load(f)
        else:
            # Search all categories
            for cat in self.combined_index.get('categories', {}).keys():
                index_file = os.path.join(
                    self.index_dir,
                    cat,
                    f"{doc_name}.json"
                )
                if os.path.exists(index_file):
                    with open(index_file, 'r') as f:
                        return json.load(f)
        
        return None
    
    def list_documents(self, category: str = None) -> List[str]:
        """
        List all available documents
        
        Args:
            category: Filter by category (optional)
        
        Returns:
            List of document names
        """
        if not self.combined_index:
            return []
        
        if category:
            return self.combined_index.get('categories', {}).get(category, [])
        
        # Return all documents
        all_docs = []
        for cat_docs in self.combined_index.get('categories', {}).values():
            all_docs.extend(cat_docs)
        
        return all_docs
    
    def get_stats(self) -> Dict:
        """Get statistics about the knowledge base"""
        if not self.combined_index:
            return {'status': 'not_loaded'}
        
        stats = {
            'status': 'loaded',
            'total_documents': self.combined_index.get('total_documents', 0),
            'categories': {}
        }
        
        for category, docs in self.combined_index.get('categories', {}).items():
            stats['categories'][category] = len(docs)
        
        return stats


def main():
    """Test the RAG query client"""
    client = RAGQueryClient()
    
    # Show stats
    print("\n📊 Knowledge Base Stats:")
    stats = client.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # List documents
    print("\n📚 Available Documents:")
    docs = client.list_documents()
    for doc in docs[:10]:  # Show first 10
        print(f"  - {doc}")
    
    if len(docs) > 10:
        print(f"  ... and {len(docs)-10} more")


if __name__ == '__main__':
    main()
