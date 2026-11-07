from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json
root=Path(__file__).parent
class Check(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.images=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if t=='a':self.links.append(a.get('href',''))
  if t=='img':self.images.append(a)
errors=[];pages={}
for f in [root/'index.html',*sorted((root/'articles').glob('*.html'))]:
 p=Check();p.feed(f.read_text());pages[f.resolve()]=p
for f,p in pages.items():
 for url in p.links:
  u=urlparse(url)
  if u.scheme or u.netloc:continue
  dest=(f.parent/unquote(u.path or f.name)).resolve()
  if dest.is_dir():dest/= 'index.html'
  if not dest.exists():errors.append(f'{f.name}: missing {url}')
  elif u.fragment and dest in pages and u.fragment not in pages[dest].ids:errors.append(f'{f.name}: missing fragment {url}')
 for im in p.images:
  if not im.get('alt'):errors.append(f'{f.name}: missing image alt')
  if not (f.parent/im.get('src','')).resolve().exists():errors.append(f'{f.name}: missing image')
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages, local links/fragments, image files/alts.')
