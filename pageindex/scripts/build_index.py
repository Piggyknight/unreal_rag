#!/usr/bin/env python3
"""
Build PageIndex for all UE documentation
Generates tree structures for all markdown documents
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict
import yaml
from dotenv import load_dotenv

# Add PageIndex to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'PageIndex'))

try:
    from run_pageindex import process_pdf, process_markdown
except ImportError:
    print("⚠️  PageIndex not found. Please clone it first:")
    print("   cd ~/Documents/unreal_rag/pageindex")
    print("   git clone https://github.com/VectifyAI/PageIndex.git")
    sys.exit(1)


class PageIndexBuilder:
    """Builds PageIndex tree structures for UE documentation"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.stats = {
            'total_docs': 0,
            'indexed': 0,
            'failed': 0,
            'errors': []
        }
        
        # Load environment variables
        load_dotenv()
        
        # Check for API key
        if not os.getenv('CHATGPT_API_KEY'):
            raise ValueError(
                "CHATGPT_API_KEY not found. Please set it in .env file:\n"
                "  echo 'CHATGPT_API_KEY=your_key_here' > .env"
            )
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def find_markdown_files(self, docs_dir: str) -> List[str]:
        """Find all markdown files in directory"""
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
        Build PageIndex for a single document
        
        Args:
            doc_path: Path to markdown file
            output_dir: Directory to save index
            category: Optional category name
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate output filename
            doc_name = Path(doc_path).stem
            if category:
                output_file = os.path.join(output_dir, category, f"{doc_name}.json")
            else:
                output_file = os.path.join(output_dir, f"{doc_name}.json")
            
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Build index using PageIndex
            print(f"  📄 Processing: {doc_name}")
            
            index_result = process_markdown(
                md_path=doc_path,
                model=self.config.get('pageindex', {}).get('model', 'gpt-4o-2024-11-20'),
                max_pages_per_node=self.config.get('pageindex', {}).get('max_pages_per_node', 10),
                max_tokens_per_node=self.config.get('pageindex', {}).get('max_tokens_per_node', 20000),
                toc_check_pages=self.config.get('pageindex', {}).get('toc_check_pages', 20),
                if_add_node_id=self.config.get('pageindex', {}).get('add_node_id', True),
                if_add_node_summary=self.config.get('pageindex', {}).get('add_node_summary', True),
                if_add_doc_description=self.config.get('pageindex', {}).get('add_doc_description', True)
            )
            
            # Save index
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(index_result, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            self.stats['errors'].append(f"{doc_path}: {str(e)}")
            return False
    
    def build_all_indexes(
        self,
        docs_dir: str,
        output_dir: str,
        categorize: bool = True
    ):
        """
        Build PageIndex for all documents
        
        Args:
            docs_dir: Directory containing markdown files
            output_dir: Directory to save indexes
            categorize: Whether to organize by category
        """
        print(f"🔍 Scanning for markdown files in {docs_dir}...")
        md_files = self.find_markdown_files(docs_dir)
        self.stats['total_docs'] = len(md_files)
        
        print(f"📄 Found {len(md_files)} documents\n")
        
        if categorize:
            # Categorize documents
            categories = self.config.get('categorization', {})
            
            for category, keywords in categories.items():
                print(f"\n📚 Processing {category}...")
                category_dir = os.path.join(output_dir, category)
                os.makedirs(category_dir, exist_ok=True)
                
                # Find matching docs
                matched_files = []
                for md_file in md_files:
                    file_lower = md_file.lower()
                    if any(keyword.lower() in file_lower for keyword in keywords):
                        matched_files.append(md_file)
                
                # Build indexes
                for md_file in matched_files:
                    if self.build_index_for_doc(md_file, category_dir, category):
                        self.stats['indexed'] += 1
                    else:
                        self.stats['failed'] += 1
        
        else:
            # Process all without categorization
            for md_file in md_files:
                if self.build_index_for_doc(md_file, output_dir):
                    self.stats['indexed'] += 1
                else:
                    self.stats['failed'] += 1
        
        self._print_summary()
        self._generate_combined_index(output_dir)
    
    def _generate_combined_index(self, output_dir: str):
        """Generate a combined index file for all documents"""
        print("\n🔄 Generating combined index...")
        
        combined_index = {
            'version': '1.0',
            'total_documents': self.stats['indexed'],
            'categories': {}
        }
        
        # Scan all generated indexes
        for category_dir in Path(output_dir).iterdir():
            if category_dir.is_dir():
                category_name = category_dir.name
                combined_index['categories'][category_name] = []
                
                for index_file in category_dir.glob('*.json'):
                    combined_index['categories'][category_name].append(
                        str(index_file.relative_to(output_dir))
                    )
        
        # Save combined index
        combined_file = os.path.join(output_dir, 'combined_index.json')
        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump(combined_index, f, indent=2)
        
        print(f"✅ Combined index saved to {combined_file}")
    
    def _print_summary(self):
        """Print build summary"""
        print("\n" + "="*50)
        print("📊 PageIndex Build Summary")
        print("="*50)
        print(f"Total documents:   {self.stats['total_docs']}")
        print(f"Indexed:           {self.stats['indexed']}")
        print(f"Failed:            {self.stats['failed']}")
        
        if self.stats['errors']:
            print(f"\n❌ Errors ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:5]:
                print(f"  - {error}")
        
        print("="*50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Build PageIndex for UE documentation'
    )
    parser.add_argument(
        '--config',
        default='../config/settings.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--docs-dir',
        default='../../docs/converted/markdown',
        help='Directory containing markdown files'
    )
    parser.add_argument(
        '--output',
        default='../generated_indexes',
        help='Output directory for indexes'
    )
    parser.add_argument(
        '--no-categorize',
        action='store_true',
        help='Disable document categorization'
    )
    
    args = parser.parse_args()
    
    builder = PageIndexBuilder(args.config)
    builder.build_all_indexes(
        args.docs_dir,
        args.output,
        categorize=not args.no_categorize
    )


if __name__ == '__main__':
    main()
