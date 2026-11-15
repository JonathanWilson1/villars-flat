# Le Bristol A46 — Villars-sur-Ollon

Static site for the Interhome-let flat (CH1884.783.20). Book buttons go to the My Rent link.

- Summer/winter toggle: `#summer` / `#winter` in the link (shareable; `?season=` also read), else saved choice, else by month (Oct–Apr = winter).
- Pages: `index.html`, `aiglon-beau-soleil-parents.html` (shared styles in `guide.css`).
- Photos: own (July 2025), Interhome listing (`img/ih-*`), Wikimedia Commons CC BY-SA (`img/cc-*`, credited in footer — keep credits if images stay).
- Videos: click-to-load YouTube (no-cookie) embeds, list in the `VIDEOS` object.
- Before deploy: replace `DOMAIN` in `robots.txt` and `sitemap.xml`, add `<link rel="canonical">`, submit sitemap in Search Console.
- Not deployed. Waiting on Interhome's OK to use the My Rent link and their photos.

Preview: `python3 -m http.server 8742 --bind 127.0.0.1`
