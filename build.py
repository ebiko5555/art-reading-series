import json,html,pathlib,datetime
P=pathlib.Path(__file__).resolve().parent
D=json.loads((P/'articles.json').read_text())
if isinstance(D,dict): D=D.get('articles',[])
for item in D:
 item['title']=item.get('title','').strip('《》')
e=lambda x:html.escape(str(x),quote=True)
def paragraphs(v):
 if isinstance(v,str):v=[v]
 return ''.join('<p>'+e(x)+'</p>' for x in v)
def shell(title,body,sub=False):
 root='../' if sub else './'
 return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#243a33"><meta name="description" content="手・素材・身体・記憶をめぐる美術の読み物。公式資料をたどり、作品をもう一度見るための連載。"><title>{e(title)} | 作品の、もう一歩奥へ</title><link rel="stylesheet" href="{root}style.css"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23243a33'/%3E%3Cpath d='M17 14v36m15-36v36m15-36v36' stroke='%23f5f3eb' stroke-width='2'/%3E%3C/svg%3E"></head><body id="top"><header><a class="brand" href="{root}">作品の、もう一歩奥へ<small>LOOK CLOSER, READ DEEPER</small></a><nav aria-label="主要ナビゲーション"><a href="{root}#series">連載一覧</a><a href="{root}#about">読み方</a></nav></header><main class="wrap">{body}<footer class="footer"><span>作品の、もう一歩奥へ<br>美術館・作家の資料から読み直す、小さな美術読本。</span><span>資料確認日は各話末尾に記載<br><a href="#top" class="backtop">ページの先頭へ ↑</a></span></footer></main><script src="{root}app.js"></script></body></html>'''
category_names={'hands':'手と身体','material':'素材と行為','memory':'記憶と不在','color':'色と知覚'}
def cat(a): return a.get('category','material')
hero='<div class="type-art" aria-hidden="true">見る、<br>読む。</div>'
first=D[0] if D else {}
if first.get('image',{}).get('local'):
 im=first['image'];hero=f'<img src="{e(im["local"])}" alt="{e(first["title"])}"><figcaption>{e(im.get("credit",""))}</figcaption>'
body=f'''<section class="hero"><div><div class="eyebrow">A small reader on art / 01—{len(D):02}</div><h1>知っている作品を、<br>もう一度、<br>見つめてみる。</h1><p>手の形、布の傷、空っぽの箱。<br>作品のどこを見ると、その表現が見えてくるのか。<br>公式資料をひもときながら、一作ずつ、ゆっくり読みます。</p><a class="button" href="articles/{e(first.get('id',''))}.html">第1話から読む　↗</a></div><figure class="hero-art">{hero}</figure></section><section id="series"><div class="section-title"><h2>作品をめぐる連載</h2><span id="count">{len(D)}編</span></div><p class="intro-note">順番に読んでも、気になる作品からでも。各話の「作品画像・参照ページを見る」を開いて、本文と見比べてみてください。作品画像の転載は、利用条件を確認できたものに限っています。</p><div class="tools"><input type="search" id="search" aria-label="作家名や作品名で探す" placeholder="作家・作品・気になる言葉で探す"><button class="filter" aria-pressed="true" data-filter="all">すべて</button>'''
for k,v in category_names.items():body+=f'<button class="filter" aria-pressed="false" data-filter="{k}">{v}</button>'
body+='</div><div class="entries">'
for i,a in enumerate(D):
 title=a.get('headline',a['title']);artist=a['artist'];lead=a.get('teaser',a.get('lead',''))
 body+=f'<article class="entry" data-category="{cat(a)}"><span class="num">{i+1:02}</span><div><span class="artist">{e(artist)} / {e(a.get("year",""))}</span><h3><a href="articles/{e(a["id"])}.html">{e(title)}</a></h3><p>{e(lead)}</p><span class="meta">{e(category_names.get(cat(a),cat(a)))}　・　{e(a.get("reading_minutes",6))}分で読む</span></div></article>'
body+='''</div><p id="empty" class="empty" hidden>該当する記事がありません。別の言葉で探してください。</p></section><section id="about" class="guide"><h2>答えを覚えるより、<br>見る手がかりを。</h2><div><p><strong>まず、画像を見てみる。</strong><br>各話では、視線を向けたい具体的な場所から始めます。専門用語は、その作品を理解するために必要な分だけ。</p><p><strong>資料の事実と、読み取りを分ける。</strong><br>制作年・素材などの作品情報、美術館や研究者の解釈、この読み物からの鑑賞の提案は、同じものではありません。解釈が分かれる部分も、そのまま示します。</p><p><strong>気づいたことを、重ねていく。</strong><br>これは完成した辞典ではなく、読み進める連載です。各話末尾に参照した公式ページを置き、新しい資料が確かめられたら追記できる形にしています。</p></div></section>'''
(P/'index.html').write_text(shell('美術を読む連載',body))
(P/'articles').mkdir(exist_ok=True)
for i,a in enumerate(D):
 sections=a.get('sections',[]);sources=a.get('sources',[])
 b=f'<div class="breadcrumbs"><a href="../#series">連載一覧</a>　/　第{i+1:02}話</div><section class="article-top"><div class="eyebrow">Chapter {i+1:02} / {e(category_names.get(cat(a),cat(a)))}</div><h1>{e(a.get("headline",a["title"]))}</h1><div class="artist">{e(a["artist"])}　《{e(a["title"])}》</div><p class="lead">{e(a.get("lead",""))}</p></section>'
 if a.get('updated'): b+=f'<p class="intro-note">追記：{e(a["updated"])}</p>'
 b+='<div class="article-layout"><aside class="toc" aria-label="この記事の目次">この話で読むこと<ol>'
 for j,s in enumerate(sections):b+=f'<li><a href="{chr(35)}{e(s.get("id",f"s{j}"))}">{e(s["heading"])}</a></li>'
 b+='<li><a href="#sources">資料をたどる</a></li></ol></aside><article class="reading">'
 b+='<div class="art-facts"><dl>'
 for label,key in [('作家','artist'),('作品','title'),('制作年','year'),('媒体','medium')]:
  if a.get(key):b+=f'<dt>{label}</dt><dd>{e(a[key])}</dd>'
 if a.get('museum'):b+=f'<dt>所蔵</dt><dd>{e(a["museum"])}</dd>'
 b+='</dl></div>'
 im=a.get('image',{})
 if im.get('local'):b+=f'<figure class="work-image"><img src="../{e(im["local"])}" alt="{e(im.get("alt",a["title"]))}"><figcaption>{e(im.get("credit",""))} / {e(im.get("rights",""))}</figcaption></figure>'
 image_url=im.get('url') or a.get('official_image_url') or (sources[0]['url'] if sources else '')
 if image_url:b+=f'<a class="art-link" href="{e(image_url)}" target="_blank" rel="noopener noreferrer"><strong>作品画像・参照ページを見る　↗</strong><small>別のタブで開きます。本文と見比べてご覧ください。</small></a>'
 for extra in a.get('related_images',[]):b+=f'<a class="art-link" href="{e(extra["url"])}" target="_blank" rel="noopener noreferrer"><strong>{e(extra["label"])}　↗</strong><small>別のタブで開きます。</small></a>'
 for j,s in enumerate(sections):b+=f'<section id="{e(s.get("id",f"s{j}"))}"><h2>{e(s["heading"])}</h2>{paragraphs(s.get("paragraphs",s.get("text",[])))}</section>'
 cautions=a.get('cautions',[])
 if cautions:b+='<aside class="caution"><h3>ここは、言い切らない</h3>'+paragraphs(cautions)+'</aside>'
 b+='<section id="sources"><h2>資料をたどる</h2><ol class="sources">'
 for s in sources:b+=f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s.get("label",s["url"]))} ↗</a><small>{e(s.get("note",""))}</small></li>'
 b+='</ol><p class="closing">確認日：2026年11月7日。リンク先の記事・作品解説を参照し、この読み物として要約・構成しています。全文転載ではありません。新しい資料や訂正が見つかった場合は、このページに追記します。</p></section><nav class="next-links" aria-label="前後の記事">'
 if i:b+=f'<a href="{e(D[i-1]["id"])}.html">← 前の話</a>'
 else:b+='<a href="../#series">← 連載一覧</a>'
 if i+1<len(D):b+=f'<a href="{e(D[i+1]["id"])}.html">次の話 → {e(D[i+1]["artist"])}</a>'
 else:b+='<a href="../#series">連載一覧へ →</a>'
 b+='</nav></article></div>'
 if a.get('checked'): b=b.replace('確認日：2026年11月7日。','確認日：'+e(a['checked'])+'。')
 if a.get('updated'): b=b.replace('確認日：2026年11月7日。','初稿確認：2026年11月7日。追記資料の確認：'+e(a['updated'])+'。')
 (P/'articles'/f'{a["id"]}.html').write_text(shell(a.get('headline',a['title']),b,True))
print(f'Built {len(D)} articles and index.')
