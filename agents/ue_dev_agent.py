#!/usr/bin/env python3
"""
UE Development Agent - Assists with Unreal Engine development
Uses RAG knowledge base for coding standards, API reference, and guides
"""

import os
import sys
from typing import Dict, List, Optional

# Add shared to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shared'))

from rag_client import RAGQueryClient


class UEDevAgent:
    """UE Development Assistant Agent"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize UE Dev Agent
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or '../config/settings.yaml'
        self.rag_client = RAGQueryClient(config_path=self.config_path)
        
        # Agent specializes in these categories
        self.primary_categories = [
            'coding-standards',
            'api-reference',
            'guides'
        ]
    
    def query(self, question: str) -> Dict:
        """
        Query the knowledge base for UE development assistance
        
        Args:
            question: User's question about UE development
        
        Returns:
            Dict with answer and sources
        """
        # Search knowledge base
        results = self.rag_client.search(
            query=question,
            categories=self.primary_categories,
            max_results=5
        )
        
        # Format response
        response = {
            'question': question,
            'answer': None,
            'sources': [],
            'confidence': 0.0
        }
        
        if results:
            # TODO: Use LLM to generate answer from retrieved context
            # For now, return first result
            response['answer'] = results[0].get('content', 'No answer found')
            response['sources'] = [r.get('source') for r in results]
            response['confidence'] = results[0].get('score', 0.0)
        else:
            response['answer'] = (
                "I couldn't find relevant information in the knowledge base. "
                "Please ensure documents have been indexed."
            )
        
        return response
    
    def get_coding_standard(self, topic: str) -> Optional[str]:
        """
        Get specific coding standard
        
        Args:
            topic: Topic to search (e.g., "naming", "namespaces")
        
        Returns:
            Coding standard text or None
        """
        # Search in coding-standards category
        results = self.rag_client.search(
            query=topic,
            categories=['coding-standards'],
            max_results=1
        )
        
        if results:
            return results[0].get('content')
        
        return None
    
    def get_api_reference(self, class_name: str) -> Optional[Dict]:
        """
        Get API reference for a class
        
        Args:
            class_name: UE class name (e.g., "UActorComponent")
        
        Returns:
            API documentation or None
        """
        doc = self.rag_client.get_document(class_name, category='api-reference')
        return doc
    
    def suggest_implementation(self, feature_description: str) -> Dict:
        """
        Suggest implementation approach based on UE best practices
        
        Args:
            feature_description: Description of feature to implement
        
        Returns:
            Implementation suggestions
        """
        # TODO: Implement using RAG + LLM
        pass


def main():
    """Test the UE Dev Agent"""
    agent = UEDevAgent()
    
    # Test queries
    test_queries = [
        "What is the coding standard for subsystems?",
        "How do I use UActorComponent?",
        "What are the naming conventions?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Q: {query}")
        print('='*60)
        
        result = agent.query(query)
        
        print(f"A: {result['answer']}")
        if result['sources']:
            print(f"\nSources: {', '.join(result['sources'])}")


if __name__ == '__main__':
    main()
