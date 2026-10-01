"""Builds index.html — the 2017–2023 portfolio deck in the H_mix (D × E) style.

Run `python3 mock.py` and `python3 build.py`, then `node render.mjs` to print portfolio.pdf.
Each page is 1440×810. Shaashop is intentionally left out of this edition.
"""
from html import escape

SITE = "joozoo.work"

# ── building blocks ──────────────────────────────────────────────

def nav(center, right, active=None):
    if center == "main":
        links = "".join(
            f'<span class="{"on" if l == active else ""}">{l}</span>'
            for l in ("Work", "About", "Contact"))
    else:
        a, b = center
        links = f'<span class="on">{escape(a)}</span><span>{escape(b)}</span>'
    if right == "available":
        pill = '<span class="pill"><i class="dot green"></i>Available for work</span>'
    else:
        pill = f'<span class="pill">{SITE}</span>'
    return (f'<header class="nav"><span class="mark">JK</span>'
            f'<nav>{links}</nav>{pill}</header>')


def chip(text):
    return f'<span class="cap"><i class="dot"></i>{escape(text)}</span>'


def card(img, caption=None, fit="contain", area=None, cls=""):
    style = f' style="grid-area:{area}"' if area else ""
    cap = chip(caption) if caption else ""
    if not caption:
        cls += " nocap"
    return (f'<figure class="card {fit} {cls}"{style}>{cap}'
            f'<img src="img/{img}.jpg" alt="{escape(caption or img)}"></figure>')


def sechead(num, title, desc):
    return (f'<div class="sechead"><span class="num">{num}</span>'
            f'<h2>{title}</h2><p>{desc}</p></div>')


pages = []
count = 0


def page(body, nav_html, cls=""):
    global count
    count += 1
    folio = f'<span class="folio">{count:02d}</span>' if count > 1 else ""
    pages.append(f'<section class="page {cls}">{nav_html}{body}{folio}</section>')


# ── page types ───────────────────────────────────────────────────

def opener(p, key, key_fit="cover", key_bg=None):
    chips = "".join(f'<span class="tag">{escape(c)}</span>' for c in p["tags"])
    meta = "".join(f'<div><dt>{k}</dt><dd>{escape(v)}</dd></div>' for k, v in (
        ("Client", p["client"]), ("Year", p["year"]),
        ("Role", p["role"]), ("Scope", p["scope"])))
    bg = f' style="background:{key_bg}"' if key_bg else ""
    body = f'''
    <div class="opener">
      <div class="op-text">
        <div class="bignum">{p["n"]}</div>
        <div class="tags">{chips}</div>
        <h1>{escape(p["name"])}</h1>
        <p class="lede">{p["desc"]}</p>
        <dl class="meta">{meta}</dl>
      </div>
      <figure class="key {key_fit}"{bg}>{chip(p["name"])}<img src="img/{key}.jpg" alt=""></figure>
    </div>'''
    page(body, nav(("Selected work", f'{p["n"]} / {p["name"]}'), "site"))


def overview(p, sub, label, title, desc, idea, paras, img, caption, fit="cover"):
    ps = "".join(f"<p>{t}</p>" for t in paras)
    body = f'''{sechead(sub, title, desc)}
    <div class="overview">
      <div class="ov-text"><h3>{idea}</h3>{ps}</div>
      {card(img, caption, fit, cls="ov-img")}
    </div>'''
    page(body, nav((f'{p["n"]} / {p["name"]}', label), "site"))


def grid(p, sub, label, title, desc, cols, rows, areas, cells, plain=False):
    area_str = " ".join('"%s"' % a for a in areas)
    style = (f'grid-template-columns:{cols};grid-template-rows:{rows};'
             f'grid-template-areas:{area_str}')
    inner = "".join(cells)
    body = f'''{sechead(sub, title, desc)}
    <div class="tray{" plain" if plain else ""}" style='{style}'>{inner}</div>'''
    page(body, nav((f'{p["n"]} / {p["name"]}', label), "site"))


def series(p, sub, label, title, desc, items):
    cols = " ".join(["1fr"] * len(items))
    letters = "abcdefghij"[:len(items)]
    cells = [card(img, cap, area=letters[i]) for i, (img, cap) in enumerate(items)]
    grid(p, sub, label, title, desc, cols, "1fr", [" ".join(letters)], cells)


def mockup(p, sub, label, title, desc, img, caption):
    """A single full-tray mockup scene (see mock.py)."""
    grid(p, sub, label, title, desc, "1fr", "1fr", ["a"], [card(img, caption, "cover", "a")])


def steps(p, sub, label, title, desc, items, fit="cover"):
    cols = len(items)
    cells = "".join(f'''
      <div class="step">
        {card(img, letter, fit)}
        <p><b>{letter} —</b> {text}</p>
      </div>''' for letter, img, text in items)
    body = f'''{sechead(sub, title, desc)}
    <div class="steps" style="grid-template-columns:repeat({cols},1fr)">{cells}</div>'''
    page(body, nav((f'{p["n"]} / {p["name"]}', label), "site"))


# ── content ──────────────────────────────────────────────────────

PROJECTS = [
    dict(n="01", name="Reingold", tags=["Poster", "Brochure", "Fact sheet"],
         list_tags="Poster, Brochure, Fact sheet", year="2021 — 22",
         client="Reingold", role="Graphic design intern",
         scope="Event poster, PPT template, brochure, fact sheets",
         desc="A full-service strategic communications firm that launches campaigns "
              "for mission-driven organizations. I designed internal event "
              "material and public-health pieces for its clients."),
    dict(n="02", name="CAPX", tags=["Campaign", "Social media", "Poster"],
         list_tags="Campaign, Social media, Poster", year="2022",
         client="SAIC — Career & Professional Experience", role="Graphic designer",
         scope="Event campaigns, posters, email, social, banners",
         desc="SAIC’s career office prepares students and alumni for sustainable, "
              "creative lives. I built the visual campaigns for its expo, talks "
              "and panel series across print and social."),
    dict(n="03", name="Therapy Materials Vault", tags=["Workbook", "Illustration", "Print"],
         list_tags="Workbook, Illustration, Print", year="2022",
         client="Therapy Materials Vault", role="Graphic design intern",
         scope="Workbooks, flash cards, activity mats",
         desc="TMV makes effective, affordable and beautifully designed materials "
              "for therapists, helping every child make social, emotional and "
              "cognitive gains."),
    dict(n="04", name="Esri", tags=["Event", "Signage", "Social media"],
         list_tags="Event signage, Environmental, Social", year="2022",
         client="Esri", role="Graphic design intern",
         scope="Conference signage, wayfinding, kiosks, social, illustration",
         desc="The global leader in GIS software — “The Science of Where.” I designed "
              "the signage system for the Esri User Conference 2022 in San Diego, "
              "plus kiosks, social posts and illustration."),
    dict(n="05", name="Vertical", tags=["Motion", "Social media"],
         list_tags="Motion graphic, Social media", year="2022",
         client="Vertical, Incorporated", role="Graphic design intern",
         scope="Animated holiday card, social campaign",
         desc="A communications agency helping energy, infrastructure, technology "
              "and transportation companies transform the world through the power "
              "of communication."),
    dict(n="06", name="Harris Theater", tags=["Performing arts", "Print", "OOH"],
         list_tags="Dance season, Print, OOH", year="2022 — 23",
         client="Harris Theater for Music and Dance", role="Graphic design intern",
         scope="Postcards, magazine ads, city panels",
         desc="Chicago’s home for music and dance in Millennium Park. I designed "
              "season campaign pieces for its 22/23 dance programme."),
]
P = {p["n"]: p for p in PROJECTS}

# 01 — cover
rows = "".join(f'''
  <li><span class="n">{p["n"]}</span><span class="t">{escape(p["name"])}</span>
  <span class="c">{escape(p["list_tags"])}</span><span class="y">{p["year"]}</span>
  <span class="a">→</span></li>''' for p in PROJECTS)
page(f'''
<div class="cover">
  <div class="hero">
    <div class="hi">Hi, I’m Joohyun <svg viewBox="0 0 40 14" width="40" height="14"><path d="M2 9c4-8 8 4 12-3s8 6 12 0 8-5 12 0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div>
    <h1>I turn brand ideas into<br><span class="hl">visual systems</span> people<br>actually <span class="mute">remember.</span></h1>
  </div>
  <aside class="hero-side">
    <p><b>Selected work, 2021 — 2023.</b> Graphic &amp; visual designer — editorial, event, campaign and digital design for agencies, nonprofits and cultural institutions.</p>
    <div class="stats"><span><b>6</b>Clients</span><span><b>4+</b>Years exp.</span><span>BFA · SAIC</span></div>
  </aside>
  <ol class="index">{rows}</ol>
</div>''', nav("main", "available", "Work"), "is-cover")

# 02 — about
page('''
<div class="about">
  <h1>Design is precision<br><span class="mute">in disguise.</span></h1>
  <p class="about-side">I’m a graphic designer specialised in editorial design, with experience
  in packaging, layout, motion graphics, social media, and UI/UX and web design.
  I’ve worked across agency, nonprofit and cultural institutions — with organisations
  like Harris Theater, SAIC, Esri and Reingold — bringing visual clarity to complex
  communication challenges.</p>
</div>
<div class="cv">
  <div><span class="num">01</span><h3>Education</h3>
    <p><b>School of the Art Institute of Chicago</b><br>BFA in Visual Communication Design<br><span class="date">09.2019 — 05.2023</span></p>
    <p class="sub">Activities</p>
    <p>Undergraduate Exhibition, Fall 2022<br>KSA — SAIC Korean Student Association</p>
  </div>
  <div><span class="num">02</span><h3>Experience</h3>
    <ul class="xp">
      <li><b>Harris Theater</b><span>Graphic design intern</span><em>12.2022 — 2023</em></li>
      <li><b>CAPX, SAIC</b><span>Graphic designer</span><em>01.2022 — 01.2023</em></li>
      <li><b>Vertical, Inc.</b><span>Graphic design intern</span><em>09 — 12.2022</em></li>
      <li><b>Esri</b><span>Graphic design intern</span><em>06 — 09.2022</em></li>
      <li><b>Therapy Materials Vault</b><span>Graphic design intern</span><em>01 — 04.2022</em></li>
      <li><b>Reingold</b><span>Graphic design intern</span><em>09.2021 — 04.2022</em></li>
    </ul>
  </div>
  <div><span class="num">03</span><h3>Tools</h3>
    <div class="tools">
      <span>Illustrator</span><span>Photoshop</span><span>InDesign</span><span>After Effects</span>
      <span>Figma</span><span>XD</span><span>Zeplin</span><span>Lightroom</span><span>HTML / CSS</span>
      <span>PowerPoint</span><span>Word</span><span>Google Analytics</span><span>Facebook Ads</span>
    </div>
  </div>
</div>''', nav("main", "available", "About"))

# ── 01 Reingold ──
p = P["01"]
opener(p, "reingold-nba-brochure")
grid(p, "01.1", "RED Talks", "RED Talks",
     "Poster and PowerPoint template for Reingold’s intern talk programme — loud, "
     "playful type that made an internal event feel like a show.",
     "1fr 1fr", "1fr", ["a b"],
     [card("reingold-red-talks-poster", "Poster · All Grown Up", "contain", "a"),
      card("mock-reingold-red-talks-ppt", "PPT template · Now That’s What I Call RED Talks", "cover", "b")])
overview(p, "01.2", "Brochure", "NBA Mind Health",
         "A brochure on the mental-skills fundamentals, built around player voices.",
         "Big quotes, clear steps — mental health in the players’ own words.",
         ["An editorial brochure for the NBA Mind Health programme. Each spread pairs a "
          "player portrait and pull quote with a short, numbered set of practical skills.",
          "Condensed display type carries the energy of the court; a calm, structured "
          "text column keeps the guidance easy to follow."],
         "reingold-nba-brochure", "Brochure spread")
mockup(p, "01.3", "Fact sheets", "DC Health fact sheets",
       "A COVID-19 mask guidance series for DC Health — icons and plain-language "
       "do’s and don’ts that read at a glance.",
       "mock-reingold-dc-health", "Fact sheet series · 3 sheets")

# ── 02 CAPX ──
p = P["02"]
opener(p, "capx-change-in-the-field")
overview(p, "02.1", "Expo", "Expo Spring 2022",
         "The SAIC Virtual Internship + Job Expo — one identity across every touchpoint.",
         "A sunrise gradient that says “your career starts here.”",
         ["The Spring 2022 Expo brought together leading creative organisations and "
          "businesses from Chicago, the U.S. and beyond. It needed to reach students "
          "everywhere — in the hallway, the inbox and the feed.",
          "I built a warm yellow-to-coral system with dotted orbit rings and set it "
          "across roll-up banners, posters, email, web banners and social."],
         "capx-expo-rollup", "Roll-up banner")
grid(p, "02.2", "Expo system", "Poster, email &amp; banner",
     "The same gradient, date lock-up and orbit rings flexed across print and digital formats.",
     "1fr 2.2fr", "1fr 1fr", ["e p", "e b"],
     [card("capx-expo-email", "Email", area="e"),
      card("capx-expo-posters", "Poster series", area="p"),
      card("capx-expo-banner", "Web banner", area="b")])
grid(p, "02.3", "Expo social", "Expo social media",
     "A countdown and how-to series for Instagram — tips before the Expo, next steps after it.",
     "1fr", "1fr", ["a"],
     [card("mock-capx-expo-social", "Instagram · feed, post & reels", "cover", "a")])
overview(p, "02.4", "Expert Exchange", "Expert Exchange",
         "Virtual one-on-ones with creative professionals and Chicago business leaders.",
         "Faces first — the experts are the reason to sign up.",
         ["Expert Exchange connects students and alumni with professionals to talk "
          "venture ideas and future careers. The poster leads with the people: circular "
          "portraits on a pink-to-blue duotone field.",
          "A QR call-out sends students straight to Handshake to book a session."],
         "capx-expert-exchange-poster", "Poster")
grid(p, "02.5", "Expert Exchange social", "Expert Exchange social",
     "Speaker cards for Instagram and engagement posts — duotone portraits with the date up front.",
     "1fr", "1fr", ["a"],
     [card("mock-capx-ee-social", "Instagram · speaker & engage posts", "cover", "a")])
steps(p, "02.6", "Panels", "Panel posters",
      "Two talks, two tones — an institutional panel and an open conversation.",
      [("A", "capx-change-in-the-field",
        "<i>Change in the Field: Museums of 2022</i> — museum professionals on how practice has "
        "changed, internships, jobs and career paths."),
       ("B", "capx-its-alright",
        "<i>It’s Alright</i> — Dialogue I, “Practicing Expression: What Do You Wish We Knew?”")])

# ── 03 TMV ──
p = P["03"]
opener(p, "tmv-nasa-workbook")
steps(p, "03.1", "Materials", "Learning materials",
      "Three products, one goal: activities kids actually want to pick up.",
      [("A", "tmv-nasa-workbook",
        "<i>NASA collaboration</i> — a Galactic Letter Writing workbook made with NASA’s Space "
        "Communications and Navigation (SCaN)."),
       ("B", "tmv-simple-chores",
        "<i>Simple Chores</i> — 10 chore flash cards and two first/then boards as a visual schedule."),
       ("C", "tmv-easter-playdough",
        "<i>Easter PlayDough</i> — five seasonal mats with eggs, the Easter Bunny and little chicks.")])

# ── 04 Esri ──
p = P["04"]
opener(p, "esri-uc-sponsor-banner")
overview(p, "04.1", "Overview", "User Conference 2022",
         "Signage for the Esri UC 2022 at the San Diego Convention Center.",
         "One ribbon of colour, from the first counter to the last kiosk.",
         ["Thousands of attendees, dozens of rooms and a tight print deadline. The "
          "conference needed signage that was quick to read and instantly “Esri.”",
          "I extended the UC ribbon artwork into a system of counters, tabletops, "
          "freestanding signs, windjammers, meterboards and kiosks — all produced and "
          "installed on site."],
         "esri-counter-photo", "Badge pick-up counter, on site")
grid(p, "04.2", "Desks", "Check-in &amp; exhibitor desks",
     "Table signs and smart counters for the exhibitor services and employee check-in desks.",
     "1fr 1fr 1fr 1fr", "1.35fr 1fr", ["a b c d", "e e f f"],
     [card("esri-table-sign-1", "Table sign · 8.5×11″", area="a"),
      card("esri-table-sign-2", None, area="b"),
      card("esri-tabletop-badge", "Tabletop · 11×17″", area="c"),
      card("esri-tabletop-luggage", None, area="d"),
      card("esri-smart-counter-1", "Smart counter · 73×23″", area="e"),
      card("esri-counter-badge", "Smart counter", area="f")])
series(p, "04.3", "Wayfinding", "Wayfinding",
       "Freestanding signs and windjammers that point people to badges, luggage and buses.",
       [("esri-freestanding-1", "Freestanding · 38×87″"), ("esri-freestanding-2", None),
        ("esri-freestanding-3", None), ("esri-freestanding-photo", "On site"),
        ("esri-windjammer-buses", "Windjammer · 40×54″"), ("esri-windjammer-photo", "On site")])
grid(p, "04.4", "Food & lunch", "Food trucks &amp; lunch",
     "Outdoor signs for food trucks and SDCC lunch options — big type for passers-by.",
     "1fr 1fr 1fr 1fr 1fr", "1fr", ["a b c d e"],
     [card("esri-foodtrucks", "Windjammer", area="a"),
      card("esri-foodtrucks-photo", "On site", area="b"),
      card("esri-lunch-graphic", "Meterboard", area="c"),
      card("esri-lunch-photo", "On site", area="d"),
      card("esri-lunch-photo-2", None, area="e")])
grid(p, "04.5", "Executive meeting", "Executive distributor meeting",
     "A warmer, sunlit palette for the private executive reception and dinner.",
     "1fr 1fr 1fr 1fr 1fr", "1fr", ["a b c d e"],
     [card("esri-exec-meter-1", "Meterboard · 36×72″", area="a"),
      card("esri-exec-meter-2", None, area="b"),
      card("esri-exec-meter-3", None, area="c"),
      card("esri-cafe-1", "Banner stand · 24×36″", area="d"),
      card("esri-cafe-2", None, area="e")])
grid(p, "04.6", "Precon & gallery", "Precon rooms &amp; map gallery",
     "Room boards for pre-conference sessions and heavyweight prints for the Map Gallery winners.",
     "1fr 1fr 1fr 1.25fr 1.25fr", "1fr 1fr", ["a b c g h", "d e f g h"],
     [card(f"esri-precon-{i+1}", ("Covered board · 26×36″" if i == 0 else None), area="abcdef"[i])
      for i in range(6)] +
     [card("esri-map-gallery-1", "Map Gallery · 41×80″", area="g"),
      card("esri-map-gallery-2", None, area="h")])
grid(p, "04.7", "Social", "Explore the Expo",
     "Instagram posts for UC 2022 — square speaker cards and landscape feed posts.",
     "1fr", "1fr", ["a"],
     [card("mock-esri-social", "Instagram · 1200×1200 & 1200×628", "cover", "a")])
steps(p, "04.8", "Kiosks", "Partner kiosks",
      "Flex PVC inserts (39×95″) for partner kiosks in the expo hall.",
      [("A", "esri-kiosk-usda", "<i>USDA</i> — advancing scientific knowledge in agriculture."),
       ("B", "esri-kiosk-nasa", "<i>NASA</i> — the AFSI wildland fire science information hub."),
       ("C", "esri-kiosk-giscorps", "<i>URISA’s GISCorps</i> — volunteer mapping, one map at a time.")],
      fit="contain")
overview(p, "04.9", "Asia Pacific", "Asia Pacific",
         "An illustrated desktop background for Esri’s Asia Pacific team.",
         "A whole region in one flowing landscape.",
         ["Landmarks from across the region — the Sydney Opera House, a torii gate, the "
          "Taj Mahal, a junk boat — are tied together by rivers and ribbons of colour.",
          "Hand-lettered script and Esri’s palette keep it on brand on every screen."],
         "mock-esri-asia-pacific", "Desktop background")
steps(p, "04.10", "Airport", "Airport operations",
      "Safety and technologies — trade-show pieces for Esri’s airport operations team.",
      [("A", "esri-airport-popup", "<i>Single rigid pop-up</i> — 29×89″."),
       ("B", "esri-airport-easel", "<i>Tabletop easel</i> — 8.5×11″, with a QR to the full story.")],
      fit="contain")

# ── 05 Vertical ──
p = P["05"]
opener(p, "vertical-holiday-card", key_fit="contain")
overview(p, "05.1", "Holiday card", "Holiday card 2022",
         "An animated holiday card for the agency’s clients and partners.",
         "Twenty years of Christmas in Chicago.",
         ["Vertical celebrated its 20th holiday season in Chicago. I animated the city "
          "skyline in snowfall, with the Vertical rocket flying through to “Happy Holidays.”",
          "Built as a motion graphic for email and social."],
         "vertical-holiday-card", "Motion graphic", fit="contain")
mockup(p, "05.2", "Social", "Social media",
       "Service cards for Instagram and a short animation — one icon style, four colours.",
       "mock-vertical-social", "Instagram · posts & animated reel")

# ── 06 Harris Theater ──
p = P["06"]
opener(p, "harris-hamburg-city-panel", key_fit="contain", key_bg="#1a1a1a")
grid(p, "06.1", "Hamburg Ballet", "Hamburg Ballet",
     "<i>The Glass Menagerie</i> by John Neumeier — a quiet, theatrical look built from "
     "a single spotlit figure.",
     "1fr 1fr 1fr 1.35fr", "1fr 1fr", ["a b c d", "a b c e"],
     [card("harris-hamburg-city-panel", "City panel", area="a"),
      card("harris-hamburg-magazine-1", "Modern Luxury magazine", area="b"),
      card("harris-hamburg-magazine-2", None, area="c"),
      card("harris-hamburg-postcard-front", "Postcard", area="d"),
      card("harris-hamburg-postcard-back", None, area="e")])
mockup(p, "06.2", "LINES Ballet", "Alonzo King LINES Ballet",
       "City panels for <i>Deep River</i> — golden textures that echo the company’s "
       "contemporary movement.",
       "mock-harris-lines-city-panels", "City panels")

# closing — mirrors the H_mix about/contact page
page(f'''
<div class="about closing">
  <h1>Thanks for<br><span class="mute">looking.</span></h1>
  <p class="about-side">Six teams, one approach: find the clear idea, then build a
  system that carries it everywhere — from a 95-inch kiosk to a 1080-pixel post.</p>
</div>
<div class="services">
  <div><span class="num">01</span><h3>Brand &amp; campaign</h3>
    <p>Visual systems, typography and event identities built around one clear idea.</p></div>
  <div><span class="num">02</span><h3>Editorial &amp; print</h3>
    <p>Layout, art direction and illustration for brochures, posters, signage and cultural institutions.</p></div>
  <div><span class="num">03</span><h3>Digital &amp; motion</h3>
    <p>Social media, motion graphics and interface design for digital brand touchpoints.</p></div>
</div>
<div class="contact">
  <div><div class="hi light">Thanks for looking</div><h2>Let’s build something real.</h2></div>
  <div class="links">
    <a>joo2hyun@gmail.com</a>
    <span>{SITE} · linkedin.com/in/joo2hyun</span>
  </div>
</div>''', nav("main", "available", "Contact"))

# ── write ────────────────────────────────────────────────────────
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Joohyun Kim — Portfolio 2017–2023</title>
<link rel="stylesheet" href="deck.css">
</head><body>
{"".join(pages)}
</body></html>'''
open("index.html", "w").write(html)
print(f"{count} pages")
