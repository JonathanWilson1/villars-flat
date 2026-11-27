"""Generate the two school term-dates pages (English only). Run from the repo root.

Dates are copied from each school's published calendar; re-check them every summer:
  Aiglon:      https://www.aiglon.ch/fs/pages/514
  Beau Soleil: https://www.beausoleil.ch/term-dates (PDFs)
"""
import json, html

BOOK = "https://myrent.interhome.com/en/CH1884.783.20/"
DOMAIN = "https://lebristolvillars.com"

# (dates, what happens, suggested stay)
PAGES = [
  dict(
    slug="aiglon-term-dates",
    name="Aiglon College",
    short="Aiglon",
    guide="aiglon-college-accommodation.html",
    source="https://www.aiglon.ch/fs/pages/514",
    title="Aiglon College term dates 2026-27 & 2027-28 · When to stay in Villars",
    desc="Aiglon College term dates for 2026-27 and 2027-28, with the nights visiting parents usually need in Villars, from the Rest & Recharge weekend to graduation.",
    hero="img/ih-village-summer-1600.webp",
    hero_alt="Villars and Chesières with the Alps behind, in summer",
    intro="The dates below are the ones that bring families up the mountain: arrivals, term ends, the February long weekend and graduation. Next to each is the stay most parents book, so you can check the apartment's calendar for those nights.",
    years=[
      ("2026-27", [
        ("Fri 18 Dec 2026", "Autumn term ends", "Thu 17 – Fri 18 Dec"),
        ("Sun 10 Jan 2027", "Winter term begins (lessons Mon 11 Jan)", "Fri 8 – Sun 10 Jan"),
        ("Fri 19 – Mon 22 Feb 2027", "Rest &amp; Recharge long weekend", "Fri 19 – Mon 22 Feb"),
        ("Fri 19 Mar 2027", "Winter term ends", "Thu 18 – Fri 19 Mar"),
        ("Sun 11 Apr 2027", "Summer term begins (lessons Mon 12 Apr)", "Fri 9 – Sun 11 Apr"),
        ("Sat 29 May 2027", "Class of 2027 graduation", "Thu 27 – Sun 30 May"),
        ("Thu 10 Jun 2027", "Year 11 celebration ceremony", "Wed 9 – Fri 11 Jun"),
        ("Fri 18 Jun 2027", "Summer term ends", "Thu 17 – Fri 18 Jun"),
      ]),
      ("2027-28", [
        ("Fri 27 Aug 2027", "New student arrival day (term begins Sat 28 Aug)", "Thu 26 – Sun 29 Aug"),
        ("Fri 15 – Sun 31 Oct 2027", "Half-term break", "Collection and return weekends"),
        ("Fri 17 Dec 2027", "Autumn term ends", "Thu 16 – Fri 17 Dec"),
        ("Sun 9 Jan 2028", "Winter term begins (lessons Mon 10 Jan)", "Fri 7 – Sun 9 Jan"),
        ("Fri 18 – Mon 21 Feb 2028", "Rest &amp; Recharge long weekend", "Fri 18 – Mon 21 Feb"),
        ("Fri 17 Mar 2028", "Winter term ends", "Thu 16 – Fri 17 Mar"),
        ("Sun 9 Apr 2028", "Summer term begins (lessons Mon 10 Apr)", "Fri 7 – Sun 9 Apr"),
        ("Sat 27 May 2028", "Class of 2028 graduation", "Thu 25 – Sun 28 May"),
        ("Fri 16 Jun 2028", "Summer term ends", "Thu 15 – Fri 16 Jun"),
      ]),
    ],
    tips=[
      "The Rest &amp; Recharge weekend falls in the middle of the Swiss ski season, when Villars is at its busiest. Book it first.",
      "Graduation weekend fills every bed in Villars and Chesières. If you're coming, book as soon as you know.",
      "The school is about 1.5 km down Avenue Centrale from the apartment: a few minutes by car, or the local bus, which stops beside the campus.",
    ],
  ),
  dict(
    slug="beau-soleil-term-dates",
    name="Beau Soleil",
    short="Beau Soleil",
    guide="beau-soleil-accommodation.html",
    source="https://www.beausoleil.ch/term-dates",
    title="Beau Soleil term dates 2026-27 & 2027-28 · Exeats, half-terms, graduation",
    desc="Collège Alpin International Beau Soleil term dates for 2026-27 and 2027-28: exeat weekends, half-terms, parent meetings and graduation, with where to stay in Villars.",
    hero="img/ih-view-winter-2-1600.webp",
    hero_alt="Villars-sur-Ollon under fresh snow",
    intro="Beau Soleil has an exeat weekend or half-term roughly every month, plus parent meetings and graduation at the end of each year. Here they are in one list, with the stay most visiting families book, so you can check the apartment's calendar for those nights.",
    years=[
      ("2026-27", [
        ("Wed 16 – Fri 18 Dec 2026", "End of Term 1: end-of-term events and in-person parent meetings", "Wed 16 – Fri 18 Dec"),
        ("Sun 10 Jan 2027", "Students return by 6pm (lessons Mon 11 Jan)", "Fri 8 – Sun 10 Jan"),
        ("Fri 29 – Sun 31 Jan 2027", "Exeat weekend (from 1pm Friday)", "Fri 29 – Sun 31 Jan"),
        ("Fri 12 – Sun 21 Feb 2027", "Half-term or school trips", "Collection and return weekends"),
        ("Fri 12 – Sun 14 Mar 2027", "Exeat weekend", "Fri 12 – Sun 14 Mar"),
        ("Thu 25 Mar 2027", "End of Term 2 (departure from 8am)", "Wed 24 – Thu 25 Mar"),
        ("Sun 11 Apr 2027", "Students return by 6pm (lessons Mon 12 Apr)", "Fri 9 – Sun 11 Apr"),
        ("Fri 30 Apr – Sun 2 May 2027", "Exeat weekend (Grade 12 stay in school)", "Fri 30 Apr – Sun 2 May"),
        ("Fri 21 – Sun 23 May 2027", "Exeat weekend", "Fri 21 – Sun 23 May"),
        ("Wed 23 – Sat 26 Jun 2027", "End of year: in-person parent meetings, end of year for Grades 6–11, graduation", "Thu 24 – Sun 27 Jun"),
      ]),
      ("2027-28", [
        ("Fri 3 Sep 2027", "New students arrive (returning students Sat 4 Sep)", "Thu 2 – Sun 5 Sep"),
        ("Fri 24 – Sun 26 Sep 2027", "Exeat weekend", "Fri 24 – Sun 26 Sep"),
        ("Thu 21 – Sun 31 Oct 2027", "Half-term or school trips (from 4:15pm Thursday)", "Collection and return weekends"),
        ("Fri 19 – Sun 21 Nov 2027", "Exeat weekend", "Fri 19 – Sun 21 Nov"),
        ("Wed 15 – Fri 17 Dec 2027", "End of Term 1: end-of-term events and in-person parent meetings", "Wed 15 – Fri 17 Dec"),
        ("Sun 9 Jan 2028", "Students return by 6pm (lessons Mon 10 Jan)", "Fri 7 – Sun 9 Jan"),
        ("Fri 28 – Sun 30 Jan 2028", "Exeat weekend", "Fri 28 – Sun 30 Jan"),
        ("Thu 10 – Sun 20 Feb 2028", "Half-term or school trips (from 4:15pm Thursday)", "Collection and return weekends"),
        ("Fri 10 – Sun 12 Mar 2028", "Exeat weekend", "Fri 10 – Sun 12 Mar"),
        ("Thu 30 – Fri 31 Mar 2028", "End of Term 2 (lessons finish 4:15pm Thursday)", "Wed 29 – Fri 31 Mar"),
        ("Mon 17 Apr 2028", "Students return (lessons Tue 18 Apr)", "Sat 15 – Mon 17 Apr"),
        ("Fri 5 – Sun 7 May 2028", "Exeat weekend (Grade 12 stay in school)", "Fri 5 – Sun 7 May"),
        ("Fri 26 – Sun 28 May 2028", "Exeat weekend", "Fri 26 – Sun 28 May"),
        ("Wed 21 – Sat 24 Jun 2028", "End of year: parent meetings, end of year for Grades 6–11, Grade 12 graduation", "Thu 22 – Sun 25 Jun"),
      ]),
    ],
    tips=[
      "The February half-term lands in the Swiss ski holidays, the busiest weeks in Villars. Book it first.",
      "Exeat weekends start at 1pm on Friday, so a Friday and Saturday night is usually enough.",
      "The school is on Route du Village in the centre of Villars, about a 10-minute walk from the apartment, so you won't need the car.",
    ],
  ),
]

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{domain}/{hero}">
<meta property="og:type" content="article">
<meta name="theme-color" content="#16241c">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="canonical" href="{domain}/{slug}.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="guide.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="top"><div class="wrap">
  <a class="brand" href="./">Le Bristol <small>Villars</small></a>
  <a class="btn" href="{book}" rel="noopener">Check dates</a>
</div></header>

<div class="hero">
  <img src="{hero}" alt="{hero_alt}">
  <div class="wrap">
    <p class="kicker">{name} · Villars-sur-Ollon</p>
    <h1>{short} term dates <em>&amp; when to stay</em></h1>
    <p class="lede">The {name} calendar for 2026-27 and 2027-28, with the nights visiting parents usually need in Villars.</p>
  </div>
</div>

<main class="wrap" id="main" tabindex="-1">
<article>
  <p>{intro}</p>
  <p>Le Bristol A46 is a one-bedroom apartment in Villars for up to 4, with two bathrooms, two balconies and a heated indoor pool in the building. <a href="{guide}">More about staying near {short}</a>.</p>

  {tables}

  <h2>Tips for booking around {short} dates</h2>
  <ul>
    {tips}
  </ul>

  <div class="note"><p>Minimum stays and changeover days vary by season. If a short stay doesn't show, try a day either side. <a href="{book}" rel="noopener">See the apartment's calendar</a>.</p></div>

  <p class="more">Dates copied from <a href="{source}" rel="noopener">{name}'s published calendar</a> in November 2026. Schools can change their dates, so check the official calendar before you book travel. Le Bristol A46 is a privately owned apartment, let through Interhome, and is not connected with {name}.</p>
</article>
</main>

<footer>
  <a href="./">Le Bristol A46, Villars-sur-Ollon</a> · <a href="{guide}">{name} accommodation</a> · <a href="{other_slug}.html">{other_short} term dates</a> · Interhome ref. CH1884.783.20
</footer>
</body>
</html>
"""

TABLE = """<h2>{name} term dates {year}</h2>
  <div class="dates-wrap"><table class="dates">
    <thead><tr><th scope="col">Dates</th><th scope="col">What happens</th><th scope="col">Suggested stay</th></tr></thead>
    <tbody>
    {rows}
    </tbody>
  </table></div>"""

for i, p in enumerate(PAGES):
    other = PAGES[1 - i]
    tables = "\n\n  ".join(
        TABLE.format(name=p["name"], year=y, rows="\n    ".join(
            f"<tr><td>{d}</td><td>{w}</td><td>{s}</td></tr>" for d, w, s in rows))
        for y, rows in p["years"])
    ld = [
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Le Bristol A46", "item": f"{DOMAIN}/"},
        {"@type": "ListItem", "position": 2, "name": f"{p['name']} accommodation", "item": f"{DOMAIN}/{p['guide']}"},
        {"@type": "ListItem", "position": 3, "name": f"{p['short']} term dates"}]},
    ]
    out = TEMPLATE.format(
        ld=json.dumps(ld, ensure_ascii=False), book=BOOK, domain=DOMAIN, tables=tables,
        tips="\n    ".join(f"<li>{t}</li>" for t in p["tips"]),
        other_slug=other["slug"], other_short=other["short"],
        **{k: v for k, v in p.items() if k not in ("years", "tips")})
    open(f"{p['slug']}.html", "w").write(out)
    print("wrote", p["slug"])
