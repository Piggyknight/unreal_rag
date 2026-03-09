#!/usr/bin/env python3
"""
UDN to Markdown Converter - Converts Unreal Engine .udn files to markdown format
"""

import os
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import yaml
from tqdm import tqdm


class UDNToMarkdownConverter:
    """Converts UDN documentation files to Markdown format"""
    
    def __init__(self):
        self.conversion_stats = {
            'total_files': 0,
            'converted': 0,
            'errors': [],
            'skipped': 0
        }
    
    def parse_udn_header(self, content: str) -> Dict[str, str]:
        """Parse UDN file header (Availability, Title, Crumbs, Description)"""
        header = {}
        
        # Extract header fields
        patterns = {
            'availability': r'Availability:(.+?)(?=Title:|Crumbs:|Description:|\[EXCERPT|$)',
            'title': r'Title:(.+?)(?=Availability:|Crumbs:|Description:|\[EXCERPT|$)',
            'crumbs': r'Crumbs:(.+?)(?=Availability:|Title:|Description:|\[EXCERPT|$)',
            'description': r'Description:(.+?)(?=Availability:|Title:|Crumbs:|\[EXCERPT|$)',
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                if value:
                    header[field] = value
        
        return header
    
    def extract_excerpts(self, content: str) -> List[Tuple[str, str]]:
        """Extract all EXCERPT blocks with their names and content"""
        excerpts = []
        
        # Find all EXCERPT blocks
        pattern = r'\[EXCERPT:([^\]]+)\](.*?)\[/EXCERPT:\1\]'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            excerpt_name = match.group(1)
            excerpt_content = match.group(2).strip()
            excerpts.append((excerpt_name, excerpt_content))
        
        return excerpts
    
    def extract_vars(self, content: str) -> Dict[str, str]:
        """Extract all VAR blocks"""
        vars_dict = {}
        
        # Find all VAR blocks
        pattern = r'\[VAR:([^\]]+)\](.*?)\[/VAR\]'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            var_name = match.group(1)
            var_content = match.group(2).strip()
            vars_dict[var_name] = var_content
        
        return vars_dict
    
    def clean_content(self, content: str) -> str:
        """Clean and format content"""
        # Remove VAR blocks (we'll handle them separately)
        content = re.sub(r'\[VAR:[^\]]+\].*?\[/VAR\]', '', content, flags=re.DOTALL)
        
        # Remove EXCERPT tags but keep content
        content = re.sub(r'\[EXCERPT:[^\]]+\]', '', content)
        content = re.sub(r'\[/EXCERPT:[^\]]+\]', '', content)
        
        # Clean up extra whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()
    
    def convert_udn_to_markdown(self, udn_content: str, source_filename: str = None) -> str:
        """
        Convert UDN content to Markdown
        
        Args:
            udn_content: Raw UDN file content
            source_filename: Original filename for reference
        
        Returns:
            Converted markdown content
        """
        md_lines = []
        
        # Parse header
        header = self.parse_udn_header(udn_content)
        
        # Add title
        if 'title' in header:
            md_lines.append(f"# {header['title']}\n")
        elif source_filename:
            title = Path(source_filename).stem.replace('_', ' ')
            md_lines.append(f"# {title}\n")
        
        # Add metadata as comment
        md_lines.append("<!-- Document metadata -->")
        if 'availability' in header:
            md_lines.append(f"<!-- Availability: {header['availability']} -->")
        if source_filename:
            md_lines.append(f"<!-- Source: {source_filename} -->")
        md_lines.append("")
        
        # Add description
        if 'description' in header:
            md_lines.append("## Overview\n")
            md_lines.append(header['description'])
            md_lines.append("")
        
        # Process EXCERPT blocks
        excerpts = self.extract_excerpts(udn_content)
        
        if excerpts:
            md_lines.append("## Content\n")
            
            for excerpt_name, excerpt_content in excerpts:
                # Clean excerpt content
                clean_excerpt = self.clean_content(excerpt_content)
                
                if clean_excerpt:
                    # Add subsection with excerpt name
                    md_lines.append(f"### {excerpt_name}\n")
                    md_lines.append(clean_excerpt)
                    md_lines.append("")
        
        # If no excerpts, try to extract all content
        if not excerpts:
            # Remove header and process remaining content
            content_without_header = re.sub(
                r'^(Availability:|Title:|Crumbs:|Description:).*$',
                '',
                udn_content,
                flags=re.MULTILINE
            )
            clean_content = self.clean_content(content_without_header)
            
            if clean_content:
                md_lines.append("## Content\n")
                md_lines.append(clean_content)
        
        # Join all lines
        markdown = '\n'.join(md_lines)
        
        # Clean up extra newlines
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        return markdown.strip()
    
    def convert_file(self, input_path: str, output_path: str) -> bool:
        """
        Convert a single UDN file to Markdown
        
        Args:
            input_path: Path to UDN file
            output_path: Path for output Markdown file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read UDN file
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                udn_content = f.read()
            
            # Convert to Markdown
            markdown = self.convert_udn_to_markdown(
                udn_content,
                source_filename=os.path.basename(input_path)
            )
            
            # Write output
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            
            return True
            
        except Exception as e:
            self.conversion_stats['errors'].append(
                f"{input_path}: {str(e)}"
            )
            return False
    
    def convert_directory(
        self,
        input_dir: str,
        output_dir: str,
        language_filter: List[str] = None
    ):
        """
        Convert all UDN files in a directory to Markdown
        
        Args:
            input_dir: Directory containing UDN files
            output_dir: Directory for output Markdown files
            language_filter: List of languages to convert (e.g., ['INT'])
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all .udn files
        udn_files = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.udn'):
                    # Check language filter
                    if language_filter:
                        parts = file.split('.')
                        if len(parts) >= 3:
                            lang = parts[-2]
                            if lang not in language_filter:
                                continue
                    
                    udn_files.append(os.path.join(root, file))
        
        self.conversion_stats['total_files'] = len(udn_files)
        print(f"📄 Found {len(udn_files)} UDN files to convert")
        
        # Convert files with progress bar
        for udn_file in tqdm(udn_files, desc="Converting"):
            try:
                # Generate output filename
                input_rel = os.path.relpath(udn_file, input_dir)
                output_file = os.path.join(
                    output_dir,
                    input_rel.replace('.udn', '.md')
                )
                
                # Create output subdirectory if needed
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                # Convert
                if self.convert_file(udn_file, output_file):
                    self.conversion_stats['converted'] += 1
                else:
                    self.conversion_stats['skipped'] += 1
                    
            except Exception as e:
                self.conversion_stats['errors'].append(
                    f"{udn_file}: {str(e)}"
                )
                self.conversion_stats['skipped'] += 1
        
        self._print_summary()
    
    def _print_summary(self):
        """Print conversion summary"""
        print("\n" + "="*50)
        print("📊 Conversion Summary")
        print("="*50)
        print(f"Total files:       {self.conversion_stats['total_files']}")
        print(f"Converted:         {self.conversion_stats['converted']}")
        print(f"Skipped:           {self.conversion_stats['skipped']}")
        
        if self.conversion_stats['errors']:
            print(f"\n❌ Errors ({len(self.conversion_stats['errors'])}):")
            for error in self.conversion_stats['errors'][:5]:
                print(f"  - {error}")
        
        print("="*50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Convert UDN documentation to Markdown'
    )
    parser.add_argument(
        '--input',
        default='../../docs/raw/udn',
        help='Input directory containing UDN files'
    )
    parser.add_argument(
        '--output',
        default='../../docs/converted/markdown',
        help='Output directory for Markdown files'
    )
    parser.add_argument(
        '--languages',
        nargs='+',
        help='Languages to convert (e.g., INT CHN). Convert all if not specified'
    )
    
    args = parser.parse_args()
    
    converter = UDNToMarkdownConverter()
    converter.convert_directory(args.input, args.output, args.languages)


if __name__ == '__main__':
    main()
