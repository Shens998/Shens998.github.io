# -*- coding: utf-8 -*-
"""Check publication consistency, local links, public-file privacy, and IDs."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json
import re
ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ['index.html','profile.html','404.html','robots.txt','sitemap.xml','assets/style.css','assets/site.js','assets/profile.js','assets/favicon.svg','assets/publications.json','assets/scholar.json','assets/language.js','zh/index.html','zh/profile.html','zh/404.html']
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.papers=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        for key in ('href','src'):
            if key in a:self.links.append(a[key])
        if tag=='article' and a.get('class')=='publication':self.papers.append(a)
        if a.get('target')=='_blank':
            assert 'noopener' in a.get('rel','') and 'noreferrer' in a.get('rel',''), 'Unsafe external link'
def main():
    scholar=json.loads((ROOT/'assets/scholar.json').read_text(encoding='utf-8'))
    assert scholar['profile_id']=='qGDGTIIAAAAJ' and scholar['verification_method'] in ('author_supplied','direct_profile')
    for metric in scholar['metrics'].values():
        assert all(type(metric[k]) is int and metric[k]>=0 for k in ('all','since'))
        assert metric['since']<=metric['all']
    papers=json.loads((ROOT/'assets/publications.json').read_text(encoding='utf-8'))
    assert len(papers)==len({p['title'] for p in papers}), 'Duplicate paper title'
    assert all(p['group'] in ('geoai','climate','human') for p in papers)
    for name in PUBLIC:
        content=(ROOT/name).read_text(encoding='utf-8')
        # Do not print matching private values if a check fails.
        assert not re.search(r'(?<!\d)1[3-9]\d{9}(?!\d)',content), f'Potential phone number in {name}'
        assert set(re.findall(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',content)) <= {'shens@bnu.edu.cn'}, f'Unauthorized email in {name}'
        assert not any(term in content for term in ('1990.10','B-718','15810553978','江苏睢宁','中共党员','/Users/','中文详细简历-沈石.pdf')), f'Private source detail in {name}'
        if not name.endswith('.html'):continue
        page=Page();page.feed(content)
        assert len(page.ids)==len(set(page.ids)), f'Duplicate HTML ID: {name}'
        for link in page.links:
            parsed=urlsplit(link)
            if parsed.scheme or parsed.netloc:continue
            if parsed.path:
                local=(ROOT if parsed.path.startswith('/') else (ROOT/name).parent)/unquote(parsed.path.lstrip('/'))
                assert local.exists(), f'Broken local link in {name}: {link}'
            elif parsed.fragment:assert parsed.fragment in page.ids, f'Broken anchor: {link}'
        if name in ('index.html','profile.html','zh/index.html','zh/profile.html'):
            assert len(page.papers)==len(papers), f'Paper count mismatch: {name}'
            assert Counter(p['data-group'] for p in page.papers)==Counter(p['group'] for p in papers)
            for p in papers:assert p['title'] in content, f'Missing title: {name}'
    print(f'PASS: {len(PUBLIC)} public files; {len(papers)} papers in all four language pages; local links, IDs and privacy checks.')
if __name__=='__main__':main()
