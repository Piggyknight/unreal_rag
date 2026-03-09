#!/usr/bin/env python3
"""
UDN Documentation Collector - Collects .udn files from Unreal Engine Documentation
"""

import os
import shutil
import argparse
from pathlib import Path
from typing import List, Dict
import yaml
from tqdm import tqdm
import hashlib


class UDNCollector:
    """Collects .udn documentation files from Unreal Engine"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.stats = {
            'total_files': 0,
            'copied_files': 0,
            'skipped_files': 0,
            'by_language': {},
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
                'docs_path': os.path.expanduser('~/Documents/ue_56/Engine/Documentation'),
            }
        }
    
    def detect_language(self, filename: str) -> str:
        """
        Detect language from UDN filename
        Format: Filename.LANG.udn (e.g., ContentBrowser.INT.udn)
        """
        parts = filename.split('.')
        if len(parts) >= 3:
            lang = parts[-2]
            return lang
        return 'UNKNOWN'
    
    def generate_unique_filename(self, source_path: str) -> str:
        """Generate unique filename preserving structure"""
        parts = Path(source_path).parts
        
        # Find 'Documentation' in path and get structure after it
        try:
            doc_idx = parts.index('Documentation')
            relevant_parts = parts[doc_idx+1:-1]  # Exclude filename
        except ValueError:
            relevant_parts = parts[-4:-1]
        
        # Create path-based prefix
        prefix = '_'.join(relevant_parts)
        
        # Get original filename
        filename = Path(source_path).name
        
        # Add hash for uniqueness
        file_hash = hashlib.md5(source_path.encode()).hexdigest()[:8]
        
        # Construct new filename
        if prefix:
            new_name = f"{prefix}_{filename}"
        else:
            new_name = filename
        
        return new_name
    
    def collect_udn_files(self, output_dir: str, language_filter: List[str] = None):
        """
        Collect .udn files from UE Documentation
        
        Args:
            output_dir: Directory to copy files to
            language_filter: List of languages to include (e.g., ['INT', 'CHN'])
                           If None, collect all
        """
        docs_path = os.path.expanduser(self.config['unreal_engine']['docs_path'])
        
        if not os.path.exists(docs_path):
            raise FileNotFoundError(f"Unreal Engine Documentation not found: {docs_path}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🔍 Scanning {docs_path} for UDN files...")
        
        # Find all .udn files
        udn_files = []
        for root, dirs, files in os.walk(docs_path):
            for file in files:
                if file.endswith('.udn'):
                    full_path = os.path.join(root, file)
                    lang = self.detect_language(file)
                    
                    # Apply language filter if specified
                    if language_filter is None or lang in language_filter:
                        udn_files.append((full_path, lang))
                    
                    # Track language statistics
                    self.stats['by_language'][lang] = \
                        self.stats['by_language'].get(lang, 0) + 1
        
        self.stats['total_files'] = len(udn_files)
        print(f"📄 Found {len(udn_files)} UDN files")
        
        if language_filter:
            print(f"🌍 Language filter: {', '.join(language_filter)}")
        
        # Copy files
        print(f"📋 Copying to {output_dir}...")
        for source_file, lang in tqdm(udn_files, desc="Copying"):
            try:
                new_name = self.generate_unique_filename(source_file)
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
        print("📊 UDN Collection Summary")
        print("="*50)
        print(f"Total files found:    {self.stats['total_files']}")
        print(f"Successfully copied:  {self.stats['copied_files']}")
        print(f"Skipped:              {self.stats['skipped_files']}")
        
        print("\n🌍 By Language:")
        for lang, count in sorted(self.stats['by_language'].items()):
            print(f"  {lang}: {count}")
        
        if self.stats['errors']:
            print(f"\n❌ Errors ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:5]:
                print(f"  - {error}")
        
        print("="*50 + "\n")
    
    def generate_report(self, output_file: str):
        """Generate detailed report"""
        report = {
            'statistics': self.stats,
            'config': self.config
        }
        
        with open(output_file, 'w') as f:
            yaml.dump(report, f, default_flow_style=False)
        
        print(f"📝 Report saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Collect UDN documentation from Unreal Engine'
    )
    parser.add_argument(
        '--config',
        default='../config/settings.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--output',
        default='../../docs/raw/udn',
        help='Output directory for collected files'
    )
    parser.add_argument(
        '--report',
        default='../../docs/udn_collection_report.yaml',
        help='Path for collection report'
    )
    parser.add_argument(
        '--languages',
        nargs='+',
        help='Languages to collect (e.g., INT CHN JPN). Collect all if not specified'
    )
    
    args = parser.parse_args()
    
    collector = UDNCollector(args.config)
    collector.collect_udn_files(args.output, args.languages)
    collector.generate_report(args.report)


if __name__ == '__main__':
    main()
