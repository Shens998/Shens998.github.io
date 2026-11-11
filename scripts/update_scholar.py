# -*- coding: utf-8 -*-
"""Refresh a verified Scholar snapshot; never replace good data on a failed fetch."""
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
import argparse
import json
import os
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
PROFILE_ID = 'qGDGTIIAAAAJ'
PROFILE_URL = 'https://scholar.google.com/citations?user=' + PROFILE_ID + '&hl=en'
class ScholarParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.name=[]; self.affiliation=[]; self.values=[]; self.table_text=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs); state={'tag':tag, 'name':a.get('id')=='gsc_prf_in', 'affiliation':'gsc_prf_il' in a.get('class','').split(), 'table':a.get('id')=='gsc_rsb_st', 'value':'gsc_rsb_std' in a.get('class','').split(), 'text':[]}
        if tag not in {'meta','link','input','br','hr','img','wbr','source'}:self.stack.append(state)
    def handle_endtag(self, tag):
        found=next((i for i in range(len(self.stack)-1,-1,-1) if self.stack[i]['tag']==tag),None)
        if found is None:return
        for state in self.stack[found:]:
            if state['value']:self.values.append(''.join(state['text']).strip())
        del self.stack[found:]
    def handle_data(self,text):
        if any(s['name'] for s in self.stack):self.name.append(text)
        if any(s['affiliation'] for s in self.stack):self.affiliation.append(text)
        if any(s['table'] for s in self.stack):self.table_text.append(text)
        for s in self.stack:
            if s['value'] and any(t['table'] for t in self.stack):s['text'].append(text)
def parse_snapshot(document):
    parser=ScholarParser();parser.feed(document)
    name=' '.join(parser.name).strip(); affiliation=' '.join(parser.affiliation).strip()
    if not ('沈石' in name or re.search(r'\bshi\s+shen\b|\bshen\s+shi\b',name,re.I)):
        raise ValueError('Scholar identity did not match Shi Shen.')
    if not re.search(r'beijing\s+normal|bnu\.edu\.cn|北京师范',affiliation,re.I):
        raise ValueError('Scholar affiliation did not match Beijing Normal University.')
    if len(parser.values)!=6 or not all(re.fullmatch(r'\d[\d,\s]*',v) for v in parser.values):
        raise ValueError('Scholar metric table is unavailable or has changed.')
    values=[int(re.sub(r'[,\s]','',v)) for v in parser.values]
    year=re.search(r'(?:Since|自)?\s*(20\d{2})', ' '.join(parser.table_text),re.I)
    if not year:raise ValueError('Could not verify the since-year column.')
    if any(values[i+1]>values[i] for i in (0,2,4)):
        raise ValueError('Recent metrics exceed all-time metrics.')
    return {'profile_id':PROFILE_ID,'profile_url':PROFILE_URL,'name':name,'affiliation':affiliation,'verified_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),'verification_method':'direct_profile','since_year':int(year[1]),'metrics':{key:{'all':values[i],'since':values[i+1]} for key,i in [('citations',0),('h_index',2),('i10_index',4)]}}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--html',type=Path,help='Read a user-exported public Scholar HTML page instead of fetching.');args=ap.parse_args()
    try:
        if args.html:document=args.html.read_text(encoding='utf-8')
        else:
            request=Request(PROFILE_URL,headers={'User-Agent':'AcademicHomepageUpdater/1.0 (public profile snapshot)','Accept-Language':'en'})
            with urlopen(request,timeout=20) as response:document=response.read(2_000_000).decode('utf-8')
        snapshot=parse_snapshot(document)
    except Exception as error:
        print('Scholar refresh unavailable; existing snapshot unchanged. '+str(error),file=sys.stderr);return 2
    path=ROOT/'assets/scholar.json';temporary=path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');os.replace(temporary,path)
    print('Updated Scholar metrics from a verified public profile. Run scripts/sync_publications.py to rebuild both languages.');return 0
if __name__=='__main__':sys.exit(main())
