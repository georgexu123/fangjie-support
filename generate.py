#!/usr/bin/env python3
"""Generate static localized support pages; no external runtime dependencies."""
import json
from html import escape as esc
from pathlib import Path
root=Path(__file__).parent
entries=json.loads((root/'localizations.json').read_text())['localizations']
labels={'zh-Hans':'简体中文','en-US':'English','de-DE':'Deutsch','fr-FR':'Français','ja-JP':'日本語','ko-KR':'한국어'}
navs={'zh-Hans':('首页','支持','隐私政策'),'en-US':('Home','Support','Privacy'),'de-DE':('Startseite','Support','Datenschutz'),'fr-FR':('Accueil','Assistance','Confidentialité'),'ja-JP':('ホーム','サポート','プライバシー'),'ko-KR':('홈','지원','개인정보 처리방침')}
email='georgexu12345@163.com'
def paragraph(s):
 return '<p>'+esc(s).replace(email,f'<a href="mailto:{email}">{email}</a>')+'</p>'
def render(locale,kind,base):
 entry=entries[locale]; support=entry['support']; privacy=entry['privacy']; brand='方界' if locale=='zh-Hans' else 'Luma Cascade'
 title=brand if kind=='index' else entry[kind]['title']
 langs=''.join(f'<a lang="{k}" hreflang="{k}" href="{base}{k}/{kind}.html"'+(' aria-current="page"' if k==locale else '')+'>'+v+'</a>' for k,v in labels.items())
 navigation=''.join(f'<a href="{p}.html"'+(' aria-current="page"' if kind==p else '')+'>'+navs[locale][i]+'</a>' for i,p in enumerate(['index','support','privacy']))
 if kind=='support':
  content=paragraph(support['intro'])+''.join('<section><h2>'+esc(f['question'])+'</h2>'+paragraph(f['answer'])+'</section>' for f in support['faq'])+paragraph(support['contact'])
 elif kind=='privacy':
  content='<p class="meta">'+esc(privacy['effectiveDate'])+'</p>'+paragraph(privacy['intro'])+''.join('<section><h2>'+esc(s['title'])+'</h2>'+paragraph(s['body'])+'</section>' for s in privacy['sections'])+paragraph(privacy['contact'])
 else:
  content=paragraph(support['intro'])+'<div class="link-grid">'+''.join(f'<a href="{k}.html">'+esc(entry[k]['title'])+'</a>' for k in ['support','privacy'])+'</div>'
 return f'''<!doctype html>
<html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="dark"><title>{esc(title)}</title><link rel="stylesheet" href="{base}styles.css"></head>
<body><main class="shell document"><nav class="language-nav">{langs}</nav><nav class="page-nav">{navigation}</nav><header><p class="eyebrow">LUMA CASCADE</p><h1>{esc(title)}</h1></header><article class="card">{content}</article><footer><p><a href="mailto:{email}">{email}</a></p><p>© 2026 George Xu</p></footer></main></body></html>\n'''
for locale in entries:
 (root/locale).mkdir(exist_ok=True)
 for kind in ['index','support','privacy']:(root/locale/(kind+'.html')).write_text(render(locale,kind,'../'))
# Preserve existing URLs used by installed app versions, with an explicit language switch.
for kind in ['index','support','privacy']:(root/(kind+'.html')).write_text(render('zh-Hans',kind,''))
print('Generated 18 localized pages and 3 compatible root pages.')
