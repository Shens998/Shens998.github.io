# -*- coding: utf-8 -*-
"""Build English default pages from Chinese pages and explicit translations."""
from html.parser import HTMLParser
from pathlib import Path
import html
import json
import re
ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = json.loads((ROOT/'scripts/translations.json').read_text(encoding='utf-8'))
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class EnglishPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out=[]; self.in_paper=False
    def translate(self, text):
        key=text.strip()
        recent=re.fullmatch(r'(\d{4}) 年至今：([\d,]+)',key)
        if recent:return 'Since '+recent[1]+': '+recent[2]
        snapshot=re.fullmatch(r'快照日期：(\d{4}-\d{2}-\d{2})。',key)
        if snapshot:return 'Snapshot: '+snapshot[1]+'.'
        if key in TRANSLATIONS:
            return text[:len(text)-len(text.lstrip())] + TRANSLATIONS[key] + text[len(text.rstrip()):]
        if re.search('[\u4e00-\u9fff]',key) and key not in ('沈','中文'):
            raise ValueError('Missing UI translation: '+key)
        return text
    def handle_decl(self,decl):self.out.append('<!'+decl+'>')
    def handle_comment(self,text):self.out.append('<!--'+text+'-->')
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='article' and a.get('class')=='publication':self.in_paper=True
        translated=[]
        for key,value in attrs:
            if value is None:translated.append(key);continue
            if key=='lang' and tag=='html':value='en'
            if key in ('aria-label','placeholder','content','alt') and not self.in_paper:value=self.translate(value)
            if key in ('href','src') and value.startswith('../assets/'):value=value[3:]
            if key=='href' and value=='../index.html':value='index.html'
            if key=='href' and value=='../profile.html':value='profile.html'
            if tag=='a' and 'language-switch' not in a.get('class',''):
                if key=='href' and a.get('hreflang')=='en':value=Path(value).name
                if key=='href' and a.get('hreflang')=='zh-CN':value='zh/'+Path(value).name
                if key=='aria-current' and a.get('hreflang')=='zh-CN':continue
            if key=='aria-label' and self.in_paper:value=value.replace('检索文献','Find paper').replace('期刊原文','Publisher').replace('：',': ')
            if key=='href' and tag=='link' and a.get('rel')=='canonical':value=value.replace('/zh/','/')
            if key=='content' and a.get('property')=='og:url':value=value.replace('/zh/','/')
            translated.append(f'{key}="{html.escape(value,quote=True)}"')
        if tag=='a' and a.get('hreflang')=='en':translated.append('aria-current="page"')
        self.out.append('<'+tag+(' '+' '.join(translated) if translated else '')+'>')
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.out[-1]=self.out[-1][:-1]+' />'
    def handle_endtag(self,tag):
        self.out.append('</'+tag+'>')
        if tag=='article':self.in_paper=False
    def handle_data(self,text):
        if self.in_paper:
            text=text.replace('检索文献 ↗','Find paper ↗').replace('期刊原文 ↗','Publisher ↗').replace('（简历所列页码）',' (pages as listed in CV)').replace('简历所列年份：','Year listed in CV: ')
        else:text=self.translate(text)
        self.out.append(html.escape(text,quote=False))
def main():
    for name in ('index.html','profile.html','404.html'):
        parser=EnglishPage();parser.feed((ROOT/'zh'/name).read_text(encoding='utf-8'))
        content=''.join(parser.out)
        if name=='index.html':
            content=re.sub(r'<h1>.*?</h1>', '<h1>Shi Shen <span lang="zh-CN">沈石</span></h1>',content,count=1,flags=re.S)
            content=content.replace('<span>Shi Shen <i>/</i> <span class="latin">Shi Shen</span></span>','<span>Shi Shen <i>/</i> <span class="latin" lang="zh-CN">沈石</span></span>')
            content=content.replace('>Shi Shen <i>/</i> Shi Shen</a>','>Shi Shen <i>/</i> <span lang="zh-CN">沈石</span></a>')
        elif name=='profile.html':
            content=content.replace('<h1>Shi Shen <span class="latin">Shi Shen</span></h1>','<h1>Shi Shen <span class="latin" lang="zh-CN">沈石</span></h1>')
        content=content.replace('<br>', '<br> ')
        (ROOT/name).write_text(content,encoding='utf-8')
    print('Built English homepage, public CV, and 404 page from Chinese sources.')
if __name__=='__main__':main()
