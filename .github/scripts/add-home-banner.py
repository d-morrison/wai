#!/usr/bin/env python3
"""
Script to add banners to pages with links to alternative formats and changed pages.
"""

import os
import sys
import json
import re
from pathlib import Path

def get_page_title(html_path):
    """Extract the page title from an HTML file."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for h1 heading with or without chapter number
            h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
            if h1_match:
                title_html = h1_match.group(1)
                # Remove chapter number span if present
                title_html = re.sub(r'<span class="chapter-number">(\d+)</span>\s*', '', title_html)
                # Strip HTML tags
                title = re.sub(r'<[^>]+>', '', title_html).strip()
                return title
            # Fall back to title tag
            title_match = re.search(r'<title>(.*?)</title>', content)
            if title_match:
                return title_match.group(1).strip()
    except Exception as e:
        print(f"  Warning: Could not extract title from {html_path}: {e}", file=sys.stderr)
    return html_path.stem

def add_page_banner(html_path, html_dir, changed_pages):
    """Add banners to a page with links to its alternative formats and changed pages."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Calculate the relative path from html_dir
    try:
        rel_path = html_path.relative_to(html_dir)
    except ValueError:
        print(f"Warning: {html_path} is not under {html_dir}", file=sys.stderr)
        return
    
    # Get the stem (filename without extension)
    stem = html_path.stem
    
    banners = []
    
    # Banner 1: Changed pages (if any exist)
    if changed_pages:
        page_links = []
        for page_info in changed_pages:
            page_rel_path = page_info['rel_path']
            page_html_path = html_dir / page_rel_path
            
            # Calculate relative link from current page to changed page
            try:
                current_dir = html_path.parent
                link_path = os.path.relpath(page_html_path, current_dir)
                page_links.append(f'<a href="{link_path}">{page_info["title"]}</a>')
            except Exception as e:
                print(f"  Warning: Could not create link to {page_rel_path}: {e}", file=sys.stderr)
        
        if page_links:
            links_html = ', '.join(page_links)
            banners.append(f'''
<div class="preview-changes-banner" style="background-color: #fff3cd; border: 1px solid #ffc107; border-radius: 4px; padding: 12px; margin: 16px 0;">
    <p style="margin: 0;">
        <strong>📋 Changes in this PR:</strong> {links_html}
        <br>
        <strong>💡 Tip:</strong> If change highlighting is glitchy, add the <code>no-preview-highlights</code> label to this PR to disable it.
    </p>
</div>
''')
    
    # Banner 2: This page's alternative formats
    # Construct paths to alternative formats relative to the HTML file's directory
    docx_tracked_file = f"{stem}-tracked-changes.docx"
    slides_file = f"{stem}-slides.html"
    
    # Build the banner with links to alternative formats
    links = []
    
    # Check if tracked changes DOCX exists - prioritize this over regular DOCX
    docx_tracked_path = html_path.parent / docx_tracked_file
    if docx_tracked_path.exists():
        links.append(f'<a href="{docx_tracked_file}" download>📝 MS Word (tracked changes)</a>')
    
    # Check if slides file exists
    slides_path = html_path.parent / slides_file
    if slides_path.exists():
        links.append(f'<a href="{slides_file}">🎞️ Slides</a>')
    
    if links:
        links_html = ' | '.join(links)
        banners.append(f'''
<div class="preview-page-formats-banner" style="background-color: #e7f3ff; border: 1px solid #b3d9ff; border-radius: 4px; padding: 12px; margin: 16px 0;">
    <p style="margin: 0;">
        <strong>📋 Other Formats:</strong> {links_html}
    </p>
</div>
''')
    
    # Only modify if we have at least one banner
    if not banners:
        print(f"  No banners to add for {rel_path}")
        return
    
    combined_banners = '\n'.join(banners)
    
    # Find insertion point (after <main> tag)
    main_match = re.search(r'(<main[^>]*>)', html)
    if main_match:
        insertion_point = main_match.end()
        html = html[:insertion_point] + combined_banners + html[insertion_point:]
        
        # Write back
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  Added {len(banners)} banner(s) to {rel_path}")
    else:
        print(f"  Could not find insertion point for {rel_path}", file=sys.stderr)

def main():
    # Get the HTML directory
    html_dir = Path(os.getenv('HTML_DIR', './_site'))
    
    if not html_dir.exists():
        print(f"HTML directory {html_dir} does not exist", file=sys.stderr)
        return
    
    print("="*60)
    print("Adding Format Banners to Pages")
    print("="*60)
    
    # Find all pages with tracked changes DOCX files (these are the changed pages)
    changed_pages = []
    for tracked_docx in html_dir.rglob('*-tracked-changes.docx'):
        # Get the corresponding HTML file
        stem = tracked_docx.stem.replace('-tracked-changes', '')
        html_file = tracked_docx.parent / f"{stem}.html"
        
        if html_file.exists():
            try:
                rel_path = html_file.relative_to(html_dir)
                title = get_page_title(html_file)
                changed_pages.append({
                    'rel_path': rel_path,
                    'stem': stem,
                    'title': title,
                    'html_path': html_file
                })
            except Exception as e:
                print(f"  Warning: Could not process {html_file}: {e}", file=sys.stderr)
    
    if changed_pages:
        print(f"\nFound {len(changed_pages)} changed page(s):")
        for page in changed_pages:
            print(f"  - {page['title']} ({page['rel_path']})")
    else:
        print("\nNo changed pages detected (no tracked-changes DOCX files found)")
    
    # Find all HTML files recursively
    html_files = list(html_dir.rglob('*.html'))
    
    if not html_files:
        print(f"No HTML files found in {html_dir}")
        return
    
    print(f"\nProcessing {len(html_files)} HTML file(s)")
    
    # Process each HTML file
    for html_file in html_files:
        add_page_banner(html_file, html_dir, changed_pages)
    
    print("\n" + "="*60)
    print("Format banner addition complete")
    print("="*60)

if __name__ == '__main__':
    main()
