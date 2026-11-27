"""Generate the two school accommodation pages for VillarsFlat-site. Run from the repo root."""
import json, html

BOOK = "https://myrent.interhome.com/en/CH1884.783.20/"

SCHOOLS = [
  dict(
    slug="aiglon-college-accommodation",
    dates="aiglon-term-dates",
    name="Aiglon College",
    short="Aiglon",
    title="Aiglon College accommodation for parents · Le Bristol A46, Villars",
    desc="Visiting Aiglon College? A self-catering apartment for up to 4 in Villars, on the same road as the school, with two bathrooms, two balconies and an indoor pool.",
    hero="img/ih-village-summer-1600.webp",
    hero_alt="Villars and Chesières with the Alps behind, in summer",
    h1="Aiglon College <em>accommodation</em> for visiting families",
    lede="A family-sized apartment in Villars, on the same road as the Aiglon campus, for parents' weekends, exeats, arrivals and graduation.",
    where="""<p>Aiglon College's campus is at Avenue Centrale 61 in Chesières, the neighbouring village just down the hill from Villars. Le Bristol is further up the same road, at Avenue Centrale 164 in Villars. That's roughly 1.5 km: a few minutes by car, or the local bus, which stops right beside the school (stop: <em>Chesières – Aiglon College</em>).</p>
<p>So you're close enough to drop in for a match, a concert or a quick lunch, while staying in the middle of Villars, near its shops, restaurants and the station.</p>""",
    occasions=[
      ("Start of term", "Settle your child into their boarding house, then come back to a flat where you can unpack, cook and rest."),
      ("Exeat weekends", "Room for your child and a friend on the sofa bed, breakfast in your own time, and a pool downstairs."),
      ("Parents' weekends &amp; concerts", "Stay a few nights without a hotel bill for every meal."),
      ("Graduation", "Celebrate with dinner on the balcony, with the valley below."),
    ],
    faqs=[
      ("How far is the apartment from Aiglon College?", "Roughly 1.5 km along Avenue Centrale, the main road through Chesières and Villars. It's a few minutes by car, or take the local bus, which stops beside the school."),
      ("How many people does it sleep?", "Up to 4: two single beds in the bedroom and a double sofa bed in the living room. There are two bathrooms."),
      ("Can we arrive by train?", "Yes. The apartment is about 500 m from Villars station, and from Geneva Airport the train journey takes about 2 hours."),
      ("When should we book for exeats and graduation?", "As soon as the school publishes its calendar. Dates around the start and end of term, exeats and graduation are the first to go in Villars, especially in February during the ski season."),
      ("Who handles the booking?", "Interhome, the holiday-rental company, handles booking and payment. Their local office in Villars, on Avenue Centrale, looks after keys, cleaning and any help you need during your stay."),
    ],
  ),
  dict(
    slug="beau-soleil-accommodation",
    dates="beau-soleil-term-dates",
    name="Beau Soleil",
    short="Beau Soleil",
    title="Beau Soleil accommodation for parents · Le Bristol A46, Villars",
    desc="Visiting Collège Alpin International Beau Soleil? A self-catering apartment for up to 4 in Villars, a short walk from the school, with an indoor pool.",
    hero="img/ih-view-winter-2-1600.webp",
    hero_alt="Villars-sur-Ollon under fresh snow",
    h1="Beau Soleil <em>accommodation</em> for visiting families",
    lede="A family-sized apartment in the village of Villars, a short walk from Collège Alpin International Beau Soleil.",
    where="""<p>Beau Soleil (Collège Alpin International Beau Soleil) is on Route du Village in the centre of Villars-sur-Ollon. Le Bristol is at Avenue Centrale 164, about 500 m from the village centre, so the school is roughly a 10-minute walk away.</p>
<p>You can leave the car parked and walk to the school, to the village shops and restaurants, and to Villars station.</p>""",
    occasions=[
      ("Arrival day", "Settle your child in, then walk back to a flat with space to unpack and a kitchen for a simple supper."),
      ("Weekends out &amp; half-term", "A sofa bed for a sibling or friend, two bathrooms, and a heated pool in the building."),
      ("Shows, matches &amp; parents' events", "A few nights close to school without eating every meal out."),
      ("Graduation", "Celebrate with a fondue on the balcony, with the valley below."),
    ],
    faqs=[
      ("How far is the apartment from Beau Soleil?", "Beau Soleil is on Route du Village in the centre of Villars. The apartment is about 500 m from the village centre, so the walk takes roughly 10 minutes."),
      ("How many people does it sleep?", "Up to 4: two single beds in the bedroom and a double sofa bed in the living room. There are two bathrooms."),
      ("Do we need a car?", "No. The school, the shops and Villars station are all within walking distance, and in winter the free ski bus stops 20 m from the building."),
      ("When should we book?", "As soon as the school calendar is out. The start and end of term, half-terms and graduation fill Villars quickly, especially in the February ski season."),
      ("Who handles the booking?", "Interhome, the holiday-rental company, handles booking and payment. Their local office in Villars, on Avenue Centrale, looks after keys, cleaning and any help you need during your stay."),
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
<meta property="og:image" content="https://lebristolvillars.com/{hero}">
<meta property="og:type" content="article">
<meta name="theme-color" content="#16241c">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
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
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</div>

<main class="wrap" id="main" tabindex="-1">
<article>
  <p>Hotels in Villars fill quickly on school weekends, and one room gets small fast with a teenager and their friends. Le Bristol A46 is a one-bedroom apartment for up to 4, with two bathrooms, two balconies, a kitchenette and a heated indoor pool in the building. It's a quiet base where the family can spread out, with Interhome's local Villars office just along the road if you need anything.</p>

  <section class="stay">
    <img src="img/ih-living-ih-1600.webp" alt="Bright pine-panelled living room with sofa, dining table and kitchenette">
    <div>
      <h2>At a glance</h2>
      <ul class="facts">
        <li>Sleeps 4: twin bedroom and a double sofa bed</li>
        <li>2 bathrooms, 2 balconies</li>
        <li>Heated indoor pool, lift, ski room</li>
        <li>Wi-Fi, kitchenette with fondue and raclette sets</li>
        <li>500 m to Villars village and station</li>
      </ul>
      <a class="btn" href="{book}" rel="noopener">See available dates</a>
    </div>
  </section>

  <h2>Where it is, compared with {short}</h2>
  {where}

  <h2>Made for school visits</h2>
  <div class="occ">
    {occasions}
  </div>

  <h2>Getting to Villars</h2>
  <ul>
    <li><strong>From Geneva Airport by train:</strong> direct trains run along Lake Geneva to Bex, then the little mountain railway climbs up to Villars. Allow about 2 hours.</li>
    <li><strong>By car:</strong> about 1 hour 30 minutes from Geneva, leaving the motorway at Aigle or Bex. In winter, check whether you need snow chains.</li>
    <li><strong>From Zurich:</strong> allow about 3 hours by train.</li>
  </ul>

  <div class="photos">
    <img src="img/ih-bedroom-640.webp" alt="Twin bedroom" loading="lazy">
    <img src="img/ih-pool-2-640.webp" alt="Indoor pool in the building" loading="lazy">
    <img src="img/balcony-portrait-800.webp" alt="Balcony set for dinner with a mountain view" loading="lazy">
  </div>

  <h2>Questions families ask</h2>
  {faq_html}

  <div class="note"><p>Planning a visit? See the <a href="{dates}.html">{short} term dates for 2026-27 and 2027-28</a>, with the nights parents usually book.</p></div>

  <div class="note"><p>See <a href="./#winter">what's on in winter</a> and <a href="./#summer">what's on in summer</a> for things to do with your child on a weekend out.</p></div>

  <p class="more">Le Bristol A46 is a privately owned apartment, let through Interhome. We are not connected with {name}. Distances and travel times are approximate, so check timetables and the school's calendar before you travel.</p>
</article>
</main>

<footer>
  <a href="./">Le Bristol A46, Villars-sur-Ollon</a> · <a href="{other_slug}.html">{other_name} accommodation</a> · Interhome ref. CH1884.783.20
</footer>
</body>
</html>
"""

for i, s in enumerate(SCHOOLS):
    other = SCHOOLS[1 - i]
    ld = [
      {"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faqs"]]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Le Bristol A46", "item": "https://lebristolvillars.com/"},
        {"@type": "ListItem", "position": 2, "name": f"{s['name']} accommodation"}]},
    ]
    occ = "\n    ".join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in s["occasions"])
    faq = "\n  ".join(f'<details><summary><h3>{html.escape(q)}</h3></summary><p>{html.escape(a)}</p></details>' for q, a in s["faqs"])
    out = TEMPLATE.format(ld=json.dumps(ld, ensure_ascii=False), book=BOOK, occasions=occ, faq_html=faq,
                          other_slug=other["slug"], other_name=other["name"], **{k: v for k, v in s.items() if k not in ("faqs", "occasions")})
    open(f"{s['slug']}.html", "w").write(out)
    print("wrote", s["slug"])
