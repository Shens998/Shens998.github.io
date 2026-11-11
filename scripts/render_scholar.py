# -*- coding: utf-8 -*-
"""Render the public metrics snapshot into both Chinese source pages."""
from pathlib import Path
from datetime import datetime
import html
import json
import re
ROOT=Path(__file__).resolve().parents[1]
def main():
    data=json.loads((ROOT/'assets/scholar.json').read_text(encoding='utf-8'))
    cards=[]
    for key,label,english in [('citations','引用次数','Citations'),('h_index','h 指数','h-index'),('i10_index','i10 指数','i10-index')]:
        metric=data['metrics'][key]
        cards.append(f'<div class="metric-card"><dt>{label}</dt><dd>{metric["all"]:,}</dd><dd class="metric-recent">{data["since_year"]} 年至今：{metric["since"]:,}</dd></div>')
    when=data['verified_at'][:10]
    source='数据由本人提供，摘自 Google Scholar。' if data['verification_method']=='author_supplied' else '数据核验于 Google Scholar 公开主页。'
    block='<section class="scholar-section wrap" id="scholar"><div class="scholar-intro"><p class="eyebrow">SCHOLARLY IMPACT</p><h2>学术影响</h2><a class="text-link" href="'+html.escape(data['profile_url'],quote=True)+'" target="_blank" rel="noopener noreferrer">Google Scholar <span>↗</span></a><p class="metric-scope">总计 · Google Scholar</p></div><div class="scholar-content"><dl class="metrics-grid">'+''.join(cards)+'</dl><p class="source-note">'+source+' <span>快照日期：'+when+'。</span></p></div></section>'
    for filename in ('zh/index.html','zh/profile.html'):
        path=ROOT/filename;content=path.read_text(encoding='utf-8')
        content,n=re.subn(r'<!-- SCHOLAR:START -->.*?<!-- SCHOLAR:END -->',lambda _: '<!-- SCHOLAR:START -->\n'+block+'\n<!-- SCHOLAR:END -->',content,flags=re.S)
        if n!=1:raise ValueError('Missing unique Scholar insertion point: '+filename)
        path.write_text(content,encoding='utf-8')
    print('Rendered Scholar snapshot in Chinese source pages.')
if __name__=='__main__':main()
