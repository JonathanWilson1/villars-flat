#!/usr/bin/env python3
"""Translate the English pages into /<lang>/ copies.

  python tools/i18n.py extract   # English strings -> i18n/en.json (keys = hash of the English)
  python tools/i18n.py render    # i18n/<lang>.json -> <lang>/*.html (+ language switcher, hreflang, sitemap)

Edit the English pages, run `extract`, translate any keys missing from i18n/<lang>.json, then `render`.
Needs beautifulsoup4.
"""
import hashlib, json, os, re, sys, copy
from bs4 import BeautifulSoup, NavigableString, Comment, Doctype

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "aiglon-college-accommodation.html", "beau-soleil-accommodation.html"]
EN_ONLY = ["aiglon-term-dates.html", "beau-soleil-term-dates.html"]  # from tools/term_dates.py; not translated
LANGS = {  # code: (native name, dir)
    "en": ("English", "ltr"), "fr": ("Français", "ltr"), "de": ("Deutsch", "ltr"), "it": ("Italiano", "ltr"),
    "es": ("Español", "ltr"), "pt": ("Português", "ltr"), "nl": ("Nederlands", "ltr"), "ar": ("العربية", "rtl"),
    "ru": ("Русский", "ltr"), "zh": ("中文", "ltr"),
}
DOMAIN = "https://lebristolvillars.com"
BOOK = "https://myrent.interhome.com/en/CH1884.783.20/"

UNIT_TAGS = {"title", "h1", "h2", "h3", "p", "li", "dt", "dd", "summary", "cite", "a", "span", "b", "button", "strong", "blockquote"}
BLOCKERS = {"div", "p", "ul", "ol", "li", "section", "article", "img", "svg", "h1", "h2", "h3", "dl", "details", "header", "nav", "main", "footer", "script", "style", "iframe", "button"}
SKIP_PARENTS = {"script", "style", "svg"}
ATTRS = ["alt", "aria-label", "title"]
META = [("name", "description"), ("property", "og:title"), ("property", "og:description")]
LD_KEYS = {"name", "text", "description"}


def key(s): return hashlib.sha1(s.strip().encode()).hexdigest()[:10]
def has_text(s): return bool(re.search(r"[A-Za-z]", s or ""))
def soup_of(path): return BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")


def units(soup):
    """Yield ('html', tag) for translatable elements, ('text', NavigableString) for loose strings."""
    claimed = set()
    for tag in soup.find_all(True):
        if tag.name not in UNIT_TAGS or any(id(p) in claimed for p in tag.parents):
            continue
        if any(p.name in SKIP_PARENTS or (p.name == "div" and "lang" in (p.get("class") or [])) for p in tag.parents):
            continue
        if tag.find(lambda t: t.name in BLOCKERS) or not has_text(tag.get_text()):
            continue
        claimed.add(id(tag)); yield ("html", tag)
    for s in soup.find_all(string=True):
        if isinstance(s, (Comment, Doctype)) or not has_text(s): continue
        if any(id(p) in claimed for p in s.parents) or any(p.name in SKIP_PARENTS or p.name in ("head", "[document]") and False for p in s.parents):
            continue
        if any(p.name in ("script", "style", "svg") for p in s.parents): continue
        if any(p.name == "div" and "lang" in (p.get("class") or []) for p in s.parents): continue
        yield ("text", s)


def ld_strings(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in LD_KEYS and isinstance(v, str) and has_text(v): yield v
            else: yield from ld_strings(v)
    elif isinstance(obj, list):
        for v in obj: yield from ld_strings(v)


def ld_translate(obj, tr):
    if isinstance(obj, dict):
        return {k: (tr(v) if k in LD_KEYS and isinstance(v, str) and has_text(v) else ld_translate(v, tr)) for k, v in obj.items()}
    if isinstance(obj, list): return [ld_translate(v, tr) for v in obj]
    return obj


def collect(soup):
    out = {}
    for kind, u in units(soup):
        s = u.decode_contents().strip() if kind == "html" else str(u).strip()
        out[key(s)] = s
    for t in soup.find_all(True):
        for a in ATTRS:
            if has_text(t.get(a)): out[key(t[a])] = t[a].strip()
    for attr, val in META:
        m = soup.find("meta", attrs={attr: val})
        if m and has_text(m.get("content")): out[key(m["content"])] = m["content"].strip()
    for sc in soup.find_all("script", type="application/ld+json"):
        for s in ld_strings(json.loads(sc.string)): out[key(s)] = s.strip()
    return out


def extract():
    en = {}
    for p in PAGES: en.update(collect(soup_of(os.path.join(ROOT, p))))
    os.makedirs(os.path.join(ROOT, "i18n"), exist_ok=True)
    json.dump(en, open(os.path.join(ROOT, "i18n", "en.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for lang in LANGS:
        if lang == "en": continue
        f = os.path.join(ROOT, "i18n", f"{lang}.json")
        have = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
        missing = [k for k in en if k not in have]
        print(f"{lang}: {len(missing)} of {len(en)} strings missing")


def switcher(lang, page, soup):
    rel = "" if lang == "en" else "../"
    items = "".join(
        f'<a href="{rel}{"" if l == "en" else l + "/"}{page if page != "index.html" else ""}" hreflang="{l}" lang="{l}"'
        f'{" aria-current=\"true\"" if l == lang else ""}>{name}</a>'
        for l, (name, _) in LANGS.items()) or ""
    html = (f'<div class="lang"><details><summary aria-label="Language">{lang.upper()}</summary>'
            f'<div class="lang-menu">{items}</div></details></div>')
    return BeautifulSoup(html, "html.parser")


def place_switcher(soup, lang, page):
    for old in soup.select("div.lang"): old.decompose()
    sw = switcher(lang, page, soup)
    host = soup.select_one(".nav-right") or soup.select_one(".top .wrap")
    btn = host.find("a", class_="btn")
    (btn.insert_before(sw) if btn else host.append(sw))


def hreflang(soup, page, lang="en"):
    for l in soup.find_all("link", rel=["alternate", "canonical"]): l.decompose()
    head = soup.head
    path = "" if page == "index.html" else page
    for l in LANGS:
        head.append(BeautifulSoup(f'<link rel="alternate" hreflang="{l}" href="{DOMAIN}/{"" if l == "en" else l + "/"}{path}">', "html.parser"))
    head.append(BeautifulSoup(f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/{path}">', "html.parser"))
    head.append(BeautifulSoup(f'<link rel="canonical" href="{DOMAIN}/{"" if lang == "en" else lang + "/"}{path}">', "html.parser"))


def render():
    en = json.load(open(os.path.join(ROOT, "i18n", "en.json"), encoding="utf-8"))
    for page in PAGES:  # English sources get switcher + hreflang in place
        src = os.path.join(ROOT, page); s = soup_of(src)
        place_switcher(s, "en", page); hreflang(s, page)
        open(src, "w", encoding="utf-8").write(str(s))
    for lang, (_, d) in LANGS.items():
        if lang == "en": continue
        f = os.path.join(ROOT, "i18n", f"{lang}.json")
        if not os.path.exists(f): print(f"skip {lang}: no translations"); continue
        tr_map = json.load(open(f, encoding="utf-8"))
        miss = 0
        def tr(s):
            nonlocal miss
            k = key(s); v = tr_map.get(k)
            if v is None: miss += 1; return s.strip()
            return v
        os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
        for page in PAGES:
            soup = soup_of(os.path.join(ROOT, page))
            for kind, u in list(units(soup)):
                if kind == "html":
                    new = tr(u.decode_contents().strip()); u.clear()
                    for c in BeautifulSoup(new, "html.parser").contents: u.append(copy.copy(c))
                else:
                    u.replace_with(NavigableString(tr(str(u))))
            for t in soup.find_all(True):
                for a in ATTRS:
                    if has_text(t.get(a)): t[a] = tr(t[a])
            for attr, val in META:
                m = soup.find("meta", attrs={attr: val})
                if m and has_text(m.get("content")): m["content"] = tr(m["content"])
            for sc in soup.find_all("script", type="application/ld+json"):
                sc.string = json.dumps(ld_translate(json.loads(sc.string), tr), ensure_ascii=False)
            soup.html["lang"] = lang
            if d == "rtl": soup.html["dir"] = "rtl"
            for t in soup.find_all(["img", "link", "script", "a"]):
                for a in ("src", "href", "srcset"):
                    v = t.get(a)
                    if not v: continue
                    if a == "srcset": t[a] = re.sub(r"(^|,\s*)(img/)", r"\1../img/", v); continue
                    if v.startswith(("img/", "guide.css", "favicon.svg")) or v in EN_ONLY: t[a] = "../" + v
                    elif v == BOOK: t[a] = BOOK.replace("/en/", f"/{lang}/")
            for m in soup.find_all("meta", property="og:image"):
                if not m["content"].startswith("http"): m["content"] = "../" + m["content"]
            place_switcher(soup, lang, page); hreflang(soup, page, lang)
            open(os.path.join(ROOT, lang, page), "w", encoding="utf-8").write(str(soup))
        print(f"{lang}: rendered, {miss} untranslated strings fell back to English")
    urls = [f"{DOMAIN}/{'' if l == 'en' else l + '/'}{'' if p == 'index.html' else p}" for l in LANGS for p in PAGES
            if l == "en" or os.path.exists(os.path.join(ROOT, l, p))] + [f"{DOMAIN}/{p}" for p in EN_ONLY]
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")


if __name__ == "__main__":
    {"extract": extract, "render": render}[sys.argv[1]]()
