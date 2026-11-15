#!/usr/bin/env python3
"""Dependency-free check of static site assets and GitHub Pages-size constraints."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re, sys
ROOT=Path(__file__).resolve().parents[1]
MAX_SIZE=1_000_000_000  # GitHub Pages published-site cap is 1 GB
MAX_FILE=100 * 1024 * 1024  # GitHub Git file-size limit: 100 MiB
class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.paths=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag in ('img','script','iframe','source') and 'src' in d:
            self.paths.append(d['src'])
        if tag=='link' and 'href' in d: self.paths.append(d['href'])
        if tag=='a' and 'href' in d and d['href'].startswith(('./','../','/')):
            self.paths.append(d['href'])

def main():
    missing=[]
    for html in ROOT.glob('*.html'):
        p=AssetParser();p.feed(html.read_text(encoding='utf-8'))
        for raw in p.paths:
            parsed=urlsplit(raw)
            if parsed.scheme or parsed.netloc or raw.startswith(('mailto:','#','data:')): continue
            relative=unquote(parsed.path)
            dest=(ROOT/relative.lstrip('/')) if relative.startswith('/') else (html.parent/relative)
            if not dest.exists(): missing.append((html.name,raw))
    for css in ROOT.rglob('*.css'):
        for raw in re.findall(r'url\(\s*[\'\"]?([^\)\'\"]+)',css.read_text(encoding='utf-8')):
            parsed=urlsplit(raw.strip())
            if parsed.scheme or parsed.netloc or raw.startswith(('data:','#')): continue
            if not (css.parent/parsed.path).exists(): missing.append((str(css.relative_to(ROOT)),raw))
    size=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts)
    large=[p for p in ROOT.rglob('*') if p.is_file() and p.stat().st_size > MAX_FILE]
    print(f'Files total: {size/1_000_000:.2f} MB / 1,000 MB Pages limit')
    if size>MAX_SIZE: print('ERROR: site exceeds GitHub Pages size limit')
    for p in large: print(f'ERROR: file exceeds 100 MiB: {p.relative_to(ROOT)}')
    for where,path in sorted(set(missing)): print(f'MISSING: {where} -> {path}')
    if missing or large or size>MAX_SIZE:
        print(f'FAIL: {len(set(missing))} missing assets/links, {len(large)} oversized files')
        return 1
    print('PASS: all local assets found and size thresholds respected')
    return 0
if __name__=='__main__': sys.exit(main())
