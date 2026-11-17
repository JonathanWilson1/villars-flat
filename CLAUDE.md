# Le Bristol A46 — lebristolvillars.com

Static marketing site for a holiday flat in Villars-sur-Ollon, let through Interhome (object CH1884.783.20). Every book button goes to the Interhome My Rent link. **Public repo; pushing to `main` deploys** (GitHub Pages, `CNAME`, DNS at Porkbun).

## Editing
- Edit only the English pages at the root (`index.html`, `aiglon-college-accommodation.html`, `beau-soleil-accommodation.html`, `guide.css`). The `fr/ de/ it/ es/ pt/ nl/ ar/ ru/ zh/` folders are generated — never hand-edit them.
- School pages come from `tools/school_pages.py` (run from repo root); regenerating drops the language switcher/hreflang until the next render.
- After any English change: `python tools/i18n.py extract` → add the missing keys to each `i18n/<lang>.json` (keys = sha1 of the English) → `python tools/i18n.py render`. Render also rewrites hreflang, canonical, the language switcher and `sitemap.xml`. Needs `beautifulsoup4`. Arabic is RTL.
- Site URL lives in the `DOMAIN` constant in `tools/i18n.py` (also hard-coded in `tools/school_pages.py` and `robots.txt`).
- Preview: `python3 -m http.server 8742 --bind 127.0.0.1`.
- Shareable claude.ai draft: `python tools/build_artifact.py <out_dir>` (artifacts can't embed YouTube; it shows a poster + link).

## Rules
- Keep the Wikimedia CC BY-SA credits in the footer while `img/cc-*` photos are used.
- Images: WebP, `-640/-800` thumbnails and `-1600` full size; Interhome originals come from `images.interhome.group/original/<id>`.
- Nothing private in this repo (owner finances, guest names, emails) — it is public.
- Season toggle: `#summer` / `#winter` hash; default Oct–Apr = winter.
