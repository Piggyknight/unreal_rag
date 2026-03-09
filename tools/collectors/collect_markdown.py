#!/usr/bin/env python3
"""
UE Documentation Collector - Collects all markdown files from Unreal Engine source
"""

import os
import shutil
import argparse
from pathlib import Path
from typing import List, Dict
import yaml
from tqdm import tqdm
import hashlib


class DocumentationCollector:
    """Collects documentation files from Unreal Engine source tree"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.stats = {
            'total_files': 0,
            'copied_files': 0,
            'skipped_files': 0,
            'errors': []
        }
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Default config
        return {
            'unreal_engine': {
                'source_path': os.path.expanduser('~/Documents/ue_56/Engine/Source'),
            },
            'collection': {
                'markdown_extensions': ['.md', '.markdown'],
                'exclude_patterns': ['*/ThirdParty/*', '*/Plugins/*']
            }
        }
    
    def should_exclude(self, file_path: str) -> bool:
        """Check if file should be excluded based on patterns"""
        exclude_patterns = self.config['collection'].get('exclude_patterns', [])
        for pattern in exclude_patterns:
            if pattern.replace('*', '') in file_path:
                return True
        return False
    
    def generate_unique_filename(self, source_path: str, output_dir: str) -> str:
        """Generate unique filename to avoid conflicts"""
        # Get relative path components
        parts = Path(source_path).parts
        
        # Find 'Source' in path and get everything after it
        try:
            source_idx = parts.index('Source')
            relevant_parts = parts[source_idx+1:-1]  # Exclude filename
        except ValueError:
            relevant_parts = parts[-4:-1]  # Last 3 directories
        
        # Create prefix from path
        prefix = '_'.join(relevant_parts[:3])  # Max 3 levels
        
        # Get original filename
        filename = Path(source_path).stem
        
        # Add hash if needed for uniqueness
        file_hash = hashlib.md5(source_path.encode()).hexdigest()[:8]
        
        # Construct new filename
        if prefix:
            new_name = f"{prefix}_{filename}.md"
        else:
            new_name = f"{filename}.md"
        
        # Ensure uniqueness
        output_path = os.path.join(output_dir, new_name)
        if os.path.exists(output_path):
            new_name = f"{prefix}_{filename}_{file_hash}.md"
        
        return new_name
    
    def collect_markdown_files(self, output_dir: str, create_structure: bool = True):
        """
        Collect all markdown files from UE source
        
        Args:
            output_dir: Directory to copy files to
            create_structure: If True, create organized subdirectories
        """
        source_path = os.path.expanduser(self.config['unreal_engine']['source_path'])
        extensions = self.config['collection']['markdown_extensions']
        
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Unreal Engine source not found: {source_path}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🔍 Scanning {source_path} for markdown files...")
        
        # Find all markdown files
        md_files = []
        for ext in extensions:
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    if file.endswith(ext):
                        full_path = os.path.join(root, file)
                        if not self.should_exclude(full_path):
                            md_files.append(full_path)
        
        self.stats['total_files'] = len(md_files)
        print(f"📄 Found {len(md_files)} markdown files")
        
        # Copy files with progress bar
        print(f"📋 Copying to {output_dir}...")
        for source_file in tqdm(md_files, desc="Copying"):
            try:
                new_name = self.generate_unique_filename(source_file, output_dir)
                dest_file = os.path.join(output_dir, new_name)
                
                shutil.copy2(source_file, dest_file)
                self.stats['copied_files'] += 1
                
            except Exception as e:
                self.stats['errors'].append(f"{source_file}: {str(e)}")
                self.stats['skipped_files'] += 1
        
        self._print_summary()
        return self.stats
    
    def _print_summary(self):
        """Print collection summary"""
        print("\n" + "="*50)
        print("📊 Collection Summary")
        print("="*50)
        print(f"Total files found:    {self.stats['total_files']}")
        print(f"Successfully copied:  {self.stats['copied_files']}")
        print(f"Skipped:              {self.stats['skipped_files']}")
        
        if self.stats['errors']:
            print(f"\n❌ Errors ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(self.stats['errors']) > 5:
                print(f"  ... and {len(self.stats['errors'])-5} more")
        
        print("="*50 + "\n")
    
    def generate_report(self, output_file: str):
        """Generate detailed report of collected files"""
        report = {
            'statistics': self.stats,
            'config': self.config
        }
        
        with open(output_file, 'w') as f:
            yaml.dump(report, f, default_flow_style=False)
        
        print(f"📝 Report saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Collect markdown documentation from Unreal Engine source'
    )
    parser.add_argument(
        '--config',
        default='../config/settings.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--output',
        default='../../docs/raw/markdown',
        help='Output directory for collected files'
    )
    parser.add_argument(
        '--report',
        default='../../docs/collection_report.yaml',
        help='Path for collection report'
    )
    
    args = parser.parse_args()
    
    collector = DocumentationCollector(args.config)
    collector.collect_markdown_files(args.output)
    collector.generate_report(args.report)


if __name__ == '__main__':
    main()
