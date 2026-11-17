"""Build a claude.ai artifact bundle of the site: python tools/build_artifact.py <out_dir> (writes <out_dir>/../files.json). No iframes there, so the film shows a poster + link."""
import re,sys,os,shutil,json,glob
B=sys.argv[1]
LANGS=['fr','de','it','es','pt','nl','ar','ru','zh']
PAGES=['index.html','aiglon-college-accommodation.html','beau-soleil-accommodation.html']
EXTRA_CSS='''  :root{color-scheme:light}
  .reveal{opacity:1!important;transform:none!important}
  .draft{position:fixed;left:16px;bottom:16px;z-index:70;background:var(--paper);color:var(--pine);font:600 .75rem/1 var(--sans);letter-spacing:.08em;text-transform:uppercase;padding:10px 14px;border-radius:999px;box-shadow:0 8px 24px rgba(0,0,0,.2)}
  @media (max-width:900px){.draft{bottom:84px}}
</style>'''
def links(s):
    # directory links -> explicit index.html (artifact file server)
    s=re.sub(r'href="((?:\.\./)?(?:[a-z]{2}/)?)"', lambda m: f'href="{m.group(1)}index.html"', s)
    s=s.replace('href="./"','href="index.html"').replace('href="./#','href="index.html#')
    return s
def site_page(s):
    s=s.replace('</style>',EXTRA_CSS,1)
    s=re.sub(r'(<body[^>]*>)',r'\1\n<script>window.NO_EMBED=true</script>',s,1)
    s=s.replace('<div class="bookbar"','<div class="draft">Draft · feedback welcome</div>\n<div class="bookbar"',1)
    return links(s)
files={}
imgs=set()
for lang in ['']+LANGS:
    for p in PAGES:
        src=os.path.join(lang,p) if lang else p
        s=open(src,encoding='utf-8').read()
        imgs|=set(re.findall(r'img/[\w.-]+\.webp',s))
        if p=='index.html': s=site_page(s)
        else: s=links(s)
        if not lang and p=='index.html':
            head=re.search(r'<head>(.*?)</head>',s,re.S).group(1); body=re.search(r'<body[^>]*>(.*)</body>',s,re.S).group(1)
            head=re.sub(r'<meta charset[^>]*/?>\s*|<meta content="width[^>]*/?>\s*|<meta name="viewport"[^>]*/?>\s*','',head)
            head=re.sub(r'<title>.*?</title>','<title>Le Bristol A46 Villars</title>',head,1,re.S)
            open(os.path.join(B,'index.html'),'w').write(head.strip()+'\n'+body.strip()+'\n'); continue
        os.makedirs(os.path.join(B,lang),exist_ok=True)
        open(os.path.join(B,src),'w',encoding='utf-8').write(s); files[src]=src
for i in imgs: shutil.copy(i,os.path.join(B,i)); files[i]=i
for f in ['guide.css','favicon.svg']: shutil.copy(f,B); files[f]=f
json.dump(files,open(os.path.join(B,'..','files.json'),'w'))
print(len(files),'files')
