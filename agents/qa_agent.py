#!/usr/bin/env python3
"""
QA Agent - Assists with testing, debugging, and quality assurance
Uses RAG knowledge base for debugging guides, API reference, and testing docs
"""

import os
import sys
from typing import Dict, List, Optional

# Add shared to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shared'))

from rag_client import RAGQueryClient


class QAAgent:
    """QA and Debugging Assistant Agent"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize QA Agent
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or '../config/settings.yaml'
        self.rag_client = RAGQueryClient(config_path=self.config_path)
        
        # Agent specializes in these categories
        self.primary_categories = [
            'debugging',
            'api-reference',
            'guides'
        ]
    
    def query(self, question: str) -> Dict:
        """
        Query the knowledge base for debugging assistance
        
        Args:
            question: User's question about testing/debugging
        
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
            response['answer'] = results[0].get('content', 'No answer found')
            response['sources'] = [r.get('source') for r in results]
            response['confidence'] = results[0].get('score', 0.0)
        else:
            response['answer'] = (
                "I couldn't find debugging information in the knowledge base. "
                "Please ensure documents have been indexed."
            )
        
        return response
    
    def debug_error(self, error_message: str) -> Dict:
        """
        Get debugging help for an error
        
        Args:
            error_message: Error message or description
        
        Returns:
            Debugging suggestions
        """
        # TODO: Implement using RAG + LLM
        return self.query(error_message)
    
    def get_test_guidelines(self, feature_type: str) -> Optional[str]:
        """
        Get testing guidelines for a feature type
        
        Args:
            feature_type: Type of feature (e.g., "unit test", "integration")
        
        Returns:
            Testing guidelines or None
        """
        results = self.rag_client.search(
            query=f"testing {feature_type}",
            categories=['debugging', 'guides'],
            max_results=1
        )
        
        if results:
            return results[0].get('content')
        
        return None


def main():
    """Test the QA Agent"""
    agent = QAAgent()
    
    # Test queries
    test_queries = [
        "How do I debug null pointer errors?",
        "What testing framework does UE use?",
        "How to write unit tests?"
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
