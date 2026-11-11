# -*- coding: utf-8 -*-
"""Regenerate static paper lists from the public JSON catalogue."""
from pathlib import Path
from urllib.parse import quote
import html
import json
import re
ROOT = Path(__file__).resolve().parents[1]
def render(p):
    esc = html.escape
    url = 'https://doi.org/' + p['doi'] if p['doi'] else p['url'] or 'https://search.crossref.org/?q=' + quote(p['title'])
    label = 'DOI ↗' if p['doi'] else '期刊原文 ↗' if p['url'] else '检索文献 ↗'
    detail = ' · ' + esc(p['detail']) if p['detail'] else ''
    authors = esc(p['authors']).replace('Shen S', '<strong>Shen S</strong>').replace('沈石', '<strong>沈石</strong>')
    return f'''<article class="publication" data-year="{p['year']}" data-group="{esc(p['group'])}"><span class="pub-year">{p['year']}</span><div><h3>{esc(p['title'])}</h3><p class="authors">{authors}</p><p class="journal">{esc(p['journal'])}<span>{detail}</span></p></div><a class="pub-link" href="{esc(url)}" target="_blank" rel="noopener noreferrer" aria-label="{esc(label + '：' + p['title'])}">{label}</a></article>'''
def main():
    papers = sorted(json.loads((ROOT/'assets/publications.json').read_text(encoding='utf-8')), key=lambda p: -p['year'])
    markup = '\n'.join(map(render, papers))
    for filename in ('zh/index.html', 'zh/profile.html'):
        path = ROOT/filename
        content = path.read_text(encoding='utf-8')
        pattern = r'(<div id="publication-list">).*?(</div>\s*<p id="empty-state")' if filename.endswith('/index.html') else r'(<div id="profile-publications">).*?(</div>\s*<h2>参编专著)'
        content, n = re.subn(pattern, lambda m: m[1]+'\n'+markup+'\n'+m[2], content, count=1, flags=re.S)
        if n != 1:
            raise ValueError(f'Expected exactly one publication region in {filename}')
        if filename.endswith('/index.html'):
            content = re.sub(r'(<span class="heading-count">)\d+(</span>)', lambda m:m[1]+str(len(papers))+m[2], content)
        path.write_text(content, encoding='utf-8')
    import runpy
    runpy.run_path(str(ROOT/'scripts/render_scholar.py'), run_name='__main__')
    runpy.run_path(str(ROOT/'scripts/build_english.py'), run_name='__main__')
    print(f'Synchronized {len(papers)} publications in all four language pages.')
if __name__ == '__main__':
    main()
