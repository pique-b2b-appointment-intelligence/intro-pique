#!/usr/bin/env python3
"""Bouwt de persoonlijke landingspagina's voor BCS batch 4.

De vorm komt uit Componenten/lp-v2 en wordt hier niet aangeraakt. Dit script
levert alleen thema plus inhoud, precies zoals LEESMIJ.md voorschrijft.

Twee dingen die hier bewust gebeuren:

1. Het bewijs onder een bevinding is altijd een zin die letterlijk op hun eigen
   site staat, met domein en controledatum eronder. Heb ik die zin niet, dan
   toont de bevinding geen bewijsblok. Een parafrase in een citaatblok zetten is
   de duurste fout die er is, want de prospect controleert het in dertig seconden.

2. Alles wat op elke pagina hetzelfde zou zijn, roteert over varianten uit
   bcs-lp-copy.py, gekozen op een vaste hash van de bedrijfsnaam. Zonder die
   rotatie loopt de gedeelde woordmassa over de 25 procent van tellscan.py.

Gebruik:
    python3 bcs-lp-generator.py
"""
import csv, html, importlib.util, os, re, shutil, sys, unicodedata

HIER = os.path.dirname(os.path.abspath(__file__))
BCS = os.path.dirname(HIER)
UIT = os.path.join(BCS, "bcs4")
COMP = os.path.abspath(os.path.join(BCS, "..", "..", "Componenten", "lp-v2"))
GECHECKT = "17 augustus 2026"
# Het adres dat op de kaart en in de browsermockup staat. De standaard zegt dat
# Pique op een klantpagina nergens hoort te staan, en dit adres is de laatste plek
# waar dat nog gebeurt. Zodra Jeffrey een subdomein aanzet, is dit een regel:
#     BASISURL = "intro.backbonecustomerservice.com"
BASISURL = os.environ.get("BCS_LP_BASIS", "intro-pique.agency/bcs4")

spec = importlib.util.spec_from_file_location("copy", os.path.join(HIER, "bcs-lp-copy.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)


def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def kies(lijst, sleutel, offset=0):
    """Vaste keuze per bedrijf, zodat een prospect altijd dezelfde pagina krijgt."""
    h = sum((i + 1) * ord(c) for i, c in enumerate(sleutel))
    return lijst[(h + offset) % len(lijst)]


def e(s):
    return html.escape(str(s or ""), quote=True)


# ── bevindingen bouwen uit wat er letterlijk staat ────────────────
def context(fa, b, vertical):
    """Eén zin over wat dit bedrijf is, zodat een bevinding niet in het luchtledige hangt.

    Alles hier komt uit de eigen scan of uit het Fase B-dossier, dus het is na te
    lopen. Zonder deze zin leest een bevinding als een algemene waarheid over
    webshops, en dan had de prospect hem net zo goed van iemand anders kunnen krijgen.
    """
    stukken = []
    markten = int(fa.get("talen") or 0) if str(fa.get("talen") or "").isdigit() else 0
    prod = int(fa.get("producten") or 0) if str(fa.get("producten") or "").isdigit() else 0
    if markten >= 6:
        stukken.append(f"je levert in {markten} taal- en marktvarianten")
    if prod >= 300:
        stukken.append(f"het assortiment telt {prod} artikelen")
    # Splitsen op een punt die door witruimte wordt gevolgd. Splitsen op elke punt
    # knipte "22.463 Trustpilot-reviews" af tot "22" en zette dat als losse zin op
    # de pagina van Flinndal, PLNTS en Casimoda.
    tr = re.split(r"\.(?:\s|$)", (b.get("trigger") or ""))[0].strip()
    if tr and len(tr) < 130:
        stukken.append(tr[0].lower() + tr[1:])
    if not stukken:
        return ""
    zin = " en ".join(stukken[:2])
    return zin[0].upper() + zin[1:] + "."


def reviewzin(b):
    """Wat klanten er zelf over schrijven. Parafrase, dus met bronvermelding in de zin
    zelf en nooit in een citaatblok."""
    r = (b.get("reviewsignaal") or "").strip()
    if not r or len(r) < 40:
        return ""
    r = re.sub(r"^(Trustpilot|Kiyoh|Reviews?)\s*[:.]\s*", "", r)
    zin = r.split(". ")[0].strip().rstrip(".")
    if len(zin) < 25 or len(zin) > 210:
        return ""
    return "In de reviews lees ik terug: " + zin[0].lower() + zin[1:] + "."


def bevindingen(sv, fa, b, naam):
    """Maximaal drie bevindingen. Elk contextstuk wordt hoogstens een keer gebruikt,
    anders leest de pagina als een herhaling van zichzelf."""
    uit = []
    dom = sv.get("domein", "")
    ctx, rev = context(fa, b, ""), reviewzin(b)
    ctx_op = rev_op = False

    tijden = sv.get("openingstijden", "").strip()
    if tijden:
        lt = tijden.lower()
        vierdaags = "donderdag" in lt and "vrijdag" not in lt
        uren = [int(h) for h, _ in re.findall(r"(\d{1,2})[:.](\d{2})", tijden)]
        eind_uur = max(uren) if uren else 24
        if vierdaags:
            kop, mech = "De week is bij jullie vier dagen lang", kies(C.BEV_VIERDAAGS, naam)
        elif eind_uur <= 17:
            kop, mech = "De desk sluit voordat de avond begint", kies(C.BEV_AVOND, naam)
        else:
            kop, mech = "De uren staan vast, de vragen niet", kies(C.BEV_UREN, naam)
        staart = ctx if ctx else ""
        ctx_op = bool(staart)
        uit.append({"kop": kop, "tekst": (mech + " " + staart).strip(),
                    "citaat": tijden, "dom": dom, "datum": "gecontroleerd " + GECHECKT})

    belofte = sv.get("reactiebelofte", "").strip()
    if belofte:
        staart = rev if rev else (ctx if not ctx_op else "")
        if staart == rev and rev:
            rev_op = True
        elif staart:
            ctx_op = True
        uit.append({"kop": "De belofte staat er zwart op wit",
                    "tekst": (kies(C.BEV_BELOFTE, naam, 1) + " " + staart).strip(),
                    "citaat": belofte, "dom": dom, "datum": "gecontroleerd " + GECHECKT})

    if not sv.get("telefoon"):
        kanaal = []
        if sv.get("whatsapp"):
            kanaal.append("WhatsApp")
        if sv.get("chat"):
            kanaal.append("de chat")
        kanaal.append("de mail")
        uit.append({"kop": "Alles loopt via het toetsenbord",
                    "tekst": "Op de contactpagina vond ik " + " en ".join(kanaal)
                             + ", zonder telefoonlijn. " + kies(C.BEV_KANAAL, naam, 2),
                    "citaat": sv.get("email", ""), "dom": dom,
                    "datum": "gecontroleerd " + GECHECKT})

    if len(uit) < 3 and rev and not rev_op:
        rev_op = True
        uit.append({"kop": "Je klanten schrijven het zelf op",
                    "tekst": rev + " " + kies(C.BEV_REVIEWSTAART, naam, 3),
                    "citaat": "", "dom": "", "datum": ""})

    if len(uit) < 3 and ctx and not ctx_op:
        ctx_op = True
        uit.append({"kop": kies(C.BEV_SCHAAL_KOP, naam, 4),
                    "tekst": ctx + " " + kies(C.BEV_SCHAAL, naam, 5),
                    "citaat": "", "dom": "", "datum": ""})

    return uit[:3]


def kantelzin(uit, fa, naam):
    """Eén zin. Dit blok staat in displaytype, dus alles boven de vijfentwintig woorden
    wordt een muur. De vorige versie plakte alle mechanismen achter elkaar en kwam op
    veertig woorden gemiddeld."""
    koppen = " ".join(x["kop"].lower() for x in uit)
    if "toetsenbord" in koppen and "belofte" in koppen:
        groep = C.KANTEL_BELOFTE
    elif "vier dagen" in koppen or "avond" in koppen or "uren" in koppen:
        groep = C.KANTEL_UREN
    elif "toetsenbord" in koppen:
        groep = C.KANTEL_KANAAL
    else:
        groep = C.KANTEL_VOLUME
    return kies(groep, naam, 6)


def usp_blok(naam):
    """Drie kaarten met wat BCS levert. Bij Pique tonen deze drie mockups de kaart,
    de pagina en de afspraak, want die verkoopt Pique. Een prospect van BCS koopt
    geen kaarten, dus hier staat bereikbaarheid, prijs en de mens erachter."""
    vink = ('<span class="v"><svg viewBox="0 0 24 24"><path d="M20 6L9 17l-5-5"/></svg></span>')
    rijen = []
    for i, u in enumerate(kies(C.USP, naam, 20)):
        rijen.append(f"""    <article class="tp" style="--dl:.{5 + i * 17:02d}s">
      <div class="tp-vis">
        <div class="ma">
          <div class="ma-top">
            <div class="ma-dag"><b>{e(u['num'])}</b><span>{e(u['lab'])}</span></div>
            <div><strong>{e(u['titel'])}</strong><em>{e(u['sub'])}</em></div>
          </div>
          <div class="ma-rij">{vink}{e(u['rij'])}</div>
          <div class="ma-hand">{e(u['hand'])}</div>
        </div>
      </div>
      <div class="tp-num">{i + 1:02d}</div>
      <h3>{e(u['kop'])}</h3>
      <p>{e(u['p'])}</p>
    </article>
""")
    return "".join(rijen)


def vinkjes_blok(naam):
    uit = []
    for i, (kop, tekst) in enumerate(kies(C.VW, naam, 21)):
        uit.append(f'    <div style="--dl:.{55 + i * 13}s"><span>&#10003;</span>'
                   f'<b>{e(kop)}</b><p>{e(tekst)}</p></div>\n')
    return "".join(uit)


# ── de pagina ─────────────────────────────────────────────────────
SJABLOON = """<!DOCTYPE html>
<!--
  Backbone Customer Service — persoonlijke pagina voor {bedrijf}
  Vorm: Componenten/lp-v2 (ongewijzigd). Hier staat alleen thema plus inhoud.
  Gegenereerd door Klanten/BCS/lp/bcs-lp-generator.py
-->
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Backbone Customer Service voor {bedrijf}</title>
<meta name="description" content="Een persoonlijke bevinding over het klantcontact van {bedrijf}.">
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="data:image/png;base64,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">
<link rel="apple-touch-icon" href="data:image/png;base64,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">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://app.cal.com"><link rel="preconnect" href="https://cal.com">
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700&family=Caveat:wght@500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="thema-bcs.css">
<link rel="stylesheet" href="lp.css">

<script>
  window.PQ_BEDRIJF      = '{bedrijf_js}';
  window.PQ_KLANT        = 'bcs';
  window.PQ_CAMPAGNE     = 'bcs-batch4';
  window.PQ_CAL          = 'jeffrey-backbone-cs/30min';
  window.PQ_VIDEO        = 'jeffrey-staand.mp4';
  window.PQ_POSTER       = 'jeffrey-staand-poster.jpg';
  window.PQ_TRACK_URL    = '/api/t';
  window.PQ_TERUGBEL_URL = '{terugbel}';
  window.PIQUE_INTRO     = {{ {intro_velden} merk: false }};
</script>
<script src="lp-intro.js"></script>
</head>
<body>
<div class="mbar" id="mbar"></div>

<nav id="nav">
  <a href="#top" class="logo" aria-label="Backbone Customer Service" style="gap:.55rem">
    <img class="op-donker" src="bcs-logo-licht.png" alt="" width="22" height="22">
    <img class="op-licht" src="bcs-logo.png" alt="" width="22" height="22">
    <span style="font:600 1.02rem/1 'Schibsted Grotesk',system-ui,sans-serif;letter-spacing:-.02em">Backbone<span style="opacity:.55">&nbsp;CS</span></span>
  </a>
  <button class="nav-cta" data-open="sheet" data-tab="plan">{nav_cta}</button>
</nav>

<div class="rail" id="rail">
  <a href="#s1"><span class="rd"></span><span class="rl">Waarom jij</span></a>
  <a href="#s2"><span class="rd"></span><span class="rl">Wat ik zag</span></a>
  <a href="#s3"><span class="rd"></span><span class="rl">Wat dat betekent</span></a>
  <a href="#s4"><span class="rd"></span><span class="rl">Wat ik voorstel</span></a>
  <a href="#gesprek"><span class="rd"></span><span class="rl">Even bellen</span></a>
</div>

<header class="hero" id="top">
  <div class="hero-grid"></div>
  <div class="hero-inner">
    <div class="hero-left">
      <div class="slot" id="slot">
        <div class="slot-card" id="slotcard">
          <div class="h">{kaart_h}</div>
          <div class="sig">Jeffrey</div>
        </div>
        <span class="slot-tag">{slot_tag}</span>
      </div>
    </div>
    <div class="hero-right">
      <h1 class="hero-h1">{hero_h1}</h1>
      <p class="hero-sub">{hero_sub}</p>
      <div class="hero-meta">
        <span class="chip"><i></i>{n} {bevwoord}</span>
        <span class="chip">{chip_lees}</span>
        <span class="chip">Alleen voor <b>{bedrijf}</b> geschreven</span>
      </div>
      <button class="vrow" id="vrow" type="button">
        <span class="vthumb"><span class="vring"></span><img src="jeffrey-staand-poster.jpg" alt=""><span class="vplay"></span></span>
        <span><b>Liever horen dan lezen?</b>Jeffrey vat het samen in 1 minuut</span>
      </button>
      <div class="scrollcue"><i></i><span>Scroll</span></div>
    </div>
  </div>
</header>

<main class="journey" id="journey">
  <svg class="jpath" id="jpath" preserveAspectRatio="none" aria-hidden="true">
    <path class="jp-base" id="jp-base"></path>
    <path class="jp-prog" id="jp-prog"></path>
  </svg>

  <section class="chapter left" id="s1">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">Waarom jij</div>
        <h2 class="ch-kop">{s1_kop}</h2>
        <p class="ch-text">{s1_tekst}</p>
        <p class="ch-text"><strong>Dit is wat ik vond.</strong></p>
        <div class="ch-sign">Jeffrey, Backbone Customer Service</div>
      </div>
      <div class="note">{n} {dingwoord}, in deze volgorde
        <svg class="arw" viewBox="0 0 52 26"><path d="M2 5c13 0 24 5 32 14M34 19l-6-1.4M34 19l1.2-6"/></svg>
      </div>
    </div>
  </section>
{bevindingen}
  <section class="chapter center pivot" id="s3">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">Wat dat betekent</div>
        <p class="ch-pivot">{pivot}</p>
      </div>
    </div>
  </section>
</main>

<section class="ask" id="ask">
  <div class="ask-in">
    <p class="ask-hand">Zal ik je hier gewoon even over bellen?</p>
    <p class="ask-sub">{ask_sub}</p>
    <div class="ask-btns">
      <button class="btn-a" data-open="sheet" data-tab="plan">Ja, plan een gesprek</button>
      <button class="btn-b" id="askread">{ask_lees}</button>
    </div>
    <p class="ask-later">Of <button data-open="sheet" data-tab="bel">laat je nummer achter</button> en ik bel je terug.</p>
  </div>
</section>

<main class="journey" id="journey2">
  <svg class="jpath" id="jpath2" preserveAspectRatio="none" aria-hidden="true">
    <path class="jp-base" id="jp-base2"></path>
    <path class="jp-prog" id="jp-prog2"></path>
  </svg>

  <section class="chapter left">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">Wat dit kost</div>
        <h2 class="ch-kop">{rekensom_kop}</h2>
        <p class="ch-text">{rekensom}</p>
        <p class="ch-pull">{rekensom_pull}</p>
      </div>
    </div>
  </section>

  <section class="chapter right">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">Hoe het anders kan</div>
        <p class="ch-text">{anders}</p>
      </div>
    </div>
  </section>

  <section class="chapter center phase" id="s4">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">Het voorstel</div>
        <h2 class="ch-kop ch-head">Wat ik voorstel.</h2>
        <p class="ch-sub">{voorstel_sub}</p>
      </div>
    </div>
  </section>
</main>

<section class="toon" id="toon">
  <div class="toon-rij">
{usp_kaarten}  </div>

  <div class="vw">
{vinkjes}  </div>
</section>

<section class="founder" id="founder">
  <img class="fo-photo fr" src="jeffrey-dylan.jpg" alt="Jeffrey en Dylan van Backbone Customer Service">
  <div class="fr">
    <div class="fo-eyebrow">De persoon achter dit voorstel</div>
    <div class="fo-text">
      <p>{founder1}</p>
      <p>{founder2}</p>
    </div>
    <p class="fo-name">Jeffrey, Backbone Customer Service</p>
  </div>
</section>

<section class="cta" id="gesprek">
  <div class="cta-inner">
    <div class="cta-eyebrow reveal">De volgende stap</div>
    <h2 class="cta-h reveal">{cta_h}</h2>
    <p class="cta-sub reveal">{cta_sub}</p>
    <div class="cta-btns reveal">
      <button class="btn-a" data-open="sheet" data-tab="plan">Kies een moment</button>
      <button class="btn-b" style="color:rgba(var(--wit-rgb),.75);border-color:rgba(var(--wit-rgb),.2)" data-open="sheet" data-tab="bel">Laat me terugbellen</button>
    </div>
    <p class="cta-alt reveal">{cta_alt} <a href="mailto:jeffrey@backbonecustomerservice.com?subject={mailonderwerp}">Mail me een korte vraag.</a></p>
  </div>
</section>

<footer>
  <div class="ft-logo"><img src="bcs-logo.png" alt="Backbone Customer Service" width="24" height="24"></div>
  <div class="ft-meta">Backbone Customer Service &nbsp;&middot;&nbsp; <a href="mailto:jeffrey@backbonecustomerservice.com">jeffrey@backbonecustomerservice.com</a><br>&copy; 2026 Backbone Customer Service</div>
</footer>

<div class="dock" id="dock">
  <span class="dock-t">{dock}</span>
  <button class="dock-b" data-open="sheet" data-tab="plan">Plannen</button>
  <button class="dock-x" id="dockx" aria-label="Sluiten">&times;</button>
</div>

<div class="sheet" id="sheet" aria-hidden="true">
  <div class="sheet-bg" data-close></div>
  <div class="sheet-in" role="dialog" aria-modal="true" aria-label="Plan een gesprek">
    <button class="sheet-x" data-close aria-label="Sluiten">&times;</button>
    <div class="sheet-host">
      <img src="jeffrey-avatar.jpg" alt="">
      <div><div class="n">20 minuten met Jeffrey</div><div class="s">Video of telefoon, jij kiest.</div></div>
    </div>
    <div class="sheet-tabs">
      <button class="on" data-tab="plan">Zelf een moment kiezen</button>
      <button data-tab="bel">Laat mij terugbellen</button>
    </div>
    <div class="panes">
    <div class="pane on" id="pane-plan">
      <div id="cal-wrap">
        <div id="cal-embed"></div>
        <div class="cal-skel" id="calskel">
          <div class="kop"></div>
          <div class="grid"><u></u><u></u><u></u><u></u><u></u><u></u><u></u><u></u><u class="o"></u><u></u><u class="o"></u><u></u><u></u><u></u><u class="o"></u><u></u><u></u><u class="o"></u><u></u><u></u><u></u><u></u><u class="o"></u><u></u><u class="o"></u><u></u><u></u><u></u></div>
          <div class="glans"></div>
        </div>
      </div>
    </div>
    <div class="pane" id="pane-bel">
      <form id="belform">
        <div class="fld"><label for="bn">Je naam</label><input id="bn" name="naam" value="{voornaam}" required></div>
        <div class="fld"><label for="bt">Telefoonnummer</label><input id="bt" name="tel" type="tel" placeholder="06" required></div>
        <label style="display:block;font-size:.74rem;font-weight:600;color:var(--ink2);margin-bottom:.35rem">Wanneer schikt het?</label>
        <div class="slots" id="slots">
          <button type="button" data-v="Vandaag, later vanmiddag">Later vanmiddag</button>
          <button type="button" data-v="Morgenochtend">Morgenochtend</button>
          <button type="button" data-v="Morgenmiddag">Morgenmiddag</button>
          <button type="button" data-v="Deze week, maakt niet uit">Deze week, maakt niet uit</button>
        </div>
        <button class="btn-a" type="submit" style="width:100%;justify-content:center">Bel me terug</button>
        <p class="sheet-note">{sheet_note}</p>
      </form>
    </div>
    </div>
  </div>
</div>

<script src="lp-v2.js"></script>
</body>
</html>
"""

BEV_SJABLOON = """
  <section class="chapter {kant} find"{id}>
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="f-head"><div class="f-num">{nr}<span class="of">/ {tot}</span></div><div class="f-tag">Wat ik zag</div></div>
        <h2 class="f-kop">{kop}</h2>
        <p class="ch-text">{tekst}</p>{bewijs}
      </div>
    </div>
  </section>
"""

BEWIJS_SJABLOON = """
        <div class="f-bewijs">
          <p class="f-quote">'{citaat}'</p>
          <div class="f-meta"><span class="dom">{dom}</span><span class="sep"></span><span>{datum}</span></div>
        </div>"""


QR = ("<svg class='qr' viewBox='0 0 21 21' shape-rendering='crispEdges' aria-hidden='true'>"
      "<rect width='21' height='21' fill='#FEFBF4'/><g fill='#241C12'>"
      "<path d='M0 0h7v7H0z M2 2h3v3H2z' fill-rule='evenodd'/>"
      "<path d='M14 0h7v7h-7z M16 2h3v3h-3z' fill-rule='evenodd'/>"
      "<path d='M0 14h7v7H0z M2 16h3v3H2z' fill-rule='evenodd'/>"
      "<rect x='9' y='1' width='1' height='1'/><rect x='9' y='3' width='1' height='2'/>"
      "<rect x='11' y='0' width='1' height='2'/><rect x='11' y='4' width='1' height='1'/>"
      "<rect x='9' y='7' width='2' height='1'/><rect x='12' y='7' width='1' height='1'/>"
      "<rect x='0' y='9' width='2' height='1'/><rect x='3' y='9' width='1' height='1'/>"
      "<rect x='5' y='9' width='1' height='2'/><rect x='7' y='10' width='1' height='1'/>"
      "<rect x='9' y='9' width='1' height='1'/><rect x='11' y='9' width='2' height='1'/>"
      "<rect x='14' y='9' width='1' height='1'/><rect x='16' y='9' width='1' height='2'/>"
      "<rect x='18' y='9' width='1' height='1'/><rect x='20' y='10' width='1' height='1'/>"
      "<rect x='9' y='11' width='1' height='2'/><rect x='11' y='12' width='1' height='1'/>"
      "<rect x='13' y='11' width='1' height='1'/><rect x='15' y='12' width='2' height='1'/>"
      "<rect x='18' y='12' width='1' height='1'/><rect x='9' y='14' width='1' height='1'/>"
      "<rect x='11' y='14' width='1' height='2'/><rect x='13' y='15' width='1' height='1'/>"
      "<rect x='15' y='14' width='1' height='1'/><rect x='17' y='15' width='2' height='1'/>"
      "<rect x='9' y='17' width='2' height='1'/><rect x='12' y='17' width='1' height='2'/>"
      "<rect x='14' y='18' width='1' height='1'/><rect x='16' y='17' width='1' height='1'/>"
      "<rect x='18' y='18' width='2' height='1'/><rect x='9' y='20' width='1' height='1'/>"
      "<rect x='11' y='20' width='2' height='1'/><rect x='15' y='20' width='1' height='1'/>"
      "<rect x='17' y='19' width='1' height='2'/><rect x='20' y='20' width='1' height='1'/>"
      "</g></svg>")

# De namen in de prospectlijsten zijn onderweg leestekens kwijtgeraakt, omdat ze uit
# CSV-kandidatenlijsten komen. Op een handgeschreven kaart is een merknaam die net
# verkeerd staat meteen ontmaskerend, dus die zetten we hier terug.
TOONNAAM = {
    "ANNA plus NINA": "ANNA + NINA",
    "Bedrukken nl": "Bedrukken.nl",
    "Studio Ins en Outs": "Studio Ins & Outs",
    "Marcels Green Soap": "Marcel's Green Soap",
    "Harrys Horse": "Harry's Horse",
    "Bobbys Dry Gin": "Bobby's Dry Gin",
    "Babys Only": "Baby's Only",
    "Fresh n Rebel": "Fresh 'n Rebel",
    "Tumble N Dry": "Tumble 'N Dry",
    "Or Coffee": "OR Coffee Roasters",
    "MaakjeCadeau": "MaakjeCadeau.nl",
    "Foto op Hout": "FotoopHout.nl",
    "Tafels op maat": "Tafels op Maat",
    "Horren Direct": "Hordeurenwinkel",
    "Overkappingoutlet": "Overkapping-Outlet",
    "Namens Mij": "Namens Mij",
    "Little Thingz": "Little Thingz",
}

TERUGBEL = ("https://script.google.com/macros/s/AKfycby37aGED41tyit5g9IemLY07prmG6J8CIER"
            "kkrYSxl92H3aBGCCui-G2stGXMDaUNsngQ/exec")


def lees(pad, sleutel="bedrijf"):
    if not os.path.exists(pad):
        return {}
    return {r[sleutel]: r for r in csv.DictReader(open(pad, encoding="utf-8"))}


def main():
    dos = lees(os.path.join(BCS, "BCS-Batch4-Research-Dossiers.csv"))
    # Twee bronnen met dezelfde velden. De verse scan wint, en waar die leeg is
    # valt hij terug op de eerdere ronde uit Fase B. Beide zijn overgetypt van de
    # site zelf, dus beide zijn citeerbaar.
    sv = lees(os.path.join(BCS, "BCS-Batch4-Servicebeloftes.csv"))
    for naam, r in lees(os.path.join(HIER, "bcs-servicescan.csv")).items():
        oud = sv.get(naam, {})
        sv[naam] = {k: (v or oud.get(k, "")) for k, v in r.items()}
        for k, v in oud.items():
            sv[naam].setdefault(k, v)
    fa = lees(os.path.join(BCS, "BCS-Batch4-FaseA-Shortlist.csv"))
    besl = {}
    for g in ("Golf1", "Golf2", "Golf3"):
        besl.update(lees(os.path.join(BCS, f"BCS-Batch4-FaseB-{g}.csv")))

    os.makedirs(UIT, exist_ok=True)
    for f in ("lp.css", "lp-v2.js", "lp-intro.js"):
        shutil.copy(os.path.join(COMP, f), UIT)
    for f in ("thema-bcs.css", "jeffrey-staand.mp4", "jeffrey-staand-poster.jpg",
              "jeffrey-dylan.jpg", "jeffrey-avatar.jpg",
              "bcs-logo.png", "bcs-logo-licht.png", "favicon.png"):
        shutil.copy(os.path.join(HIER, f), UIT)

    # Alleen de bedrijven die ook echt een kaart krijgen. De verzendlijst is de bron
    # van waarheid: daar staat wie een gecontroleerd adres heeft.
    verzend = {r["bedrijf"] for r in csv.DictReader(
        open(os.path.join(BCS, "BCS-Batch4-Verzendlijst.csv"), encoding="utf-8"))
        if not r["klasse"].startswith("D")}
    verzendrij = {r["bedrijf"]: r for r in csv.DictReader(
        open(os.path.join(BCS, "BCS-Batch4-Verzendlijst.csv"), encoding="utf-8"))}

    urls, overzicht, zonder = [], [], []
    for naam, d in sorted(dos.items()):
        if d.get("status") == "geparkeerd-concern" or naam not in verzend:
            continue
        s = slug(naam)
        toon = TOONNAAM.get(naam, naam)
        svd = sv.get(naam, {"domein": d["domein"]})
        b = besl.get(naam, {})

        # voornaam alleen als de beslisser hard geverifieerd is
        # De voornaam komt uit de verzendlijst. Daar staat per bedrijf of de naam
        # door twee bronnen is bevestigd. Zonder naam vervalt de aanhef vanzelf.
        voornaam = ""
        vz = verzendrij.get(naam, {})
        vol = (vz.get("naam") or "").strip()
        if vol:
            eerste = re.split(r"\s+en\s+|,|/", vol)[0].strip()
            deel = eerste.split()
            if deel and deel[0][0].isupper() and len(deel[0]) > 2:
                voornaam = deel[0]

        bevs = bevindingen(svd, fa.get(naam, {}), b, naam)
        if not bevs:
            zonder.append(naam)
            continue

        blokken = []
        for i, bv in enumerate(bevs):
            bewijs = ""
            if bv["citaat"]:
                bewijs = BEWIJS_SJABLOON.format(citaat=e(bv["citaat"]), dom=e(bv["dom"]),
                                                datum=e(bv["datum"]))
            blokken.append(BEV_SJABLOON.format(
                kant="right" if i % 2 == 0 else "left",
                id=' id="s2"' if i == 0 else "",
                nr=f"{i+1:02d}", tot=f"{len(bevs):02d}",
                kop=e(bv["kop"]), tekst=bv["tekst"], bewijs=bewijs))

        km = d.get("koopmoment", "Het volume groeit sneller dan de bezetting")
        kaart_h = (f"Hoi {e(voornaam)}.<br>Ik keek een tijd naar <em>{e(toon)}</em>."
                   if voornaam else f"Ik keek een tijd<br>naar <em>{e(toon)}</em>.")
        # ctaSub moet mee, anders valt lp-intro.js terug op "Video van Simon" en
        # staat er Pique op een klantpagina. De video van Jeffrey duurt 1:01.
        intro = ((f"voornaam: '{voornaam}', " if voornaam else "")
                 + f"bedrijf: '{e(toon)}', "
                 + "ctaSub: 'Video van Jeffrey \u00b7 1 minuut',")

        pagina = SJABLOON.format(
            bedrijf=e(toon), bedrijf_js=toon.replace("'", "\\'"),
            terugbel=TERUGBEL, intro_velden=intro,
            kaart_h=kaart_h,
            hero_sub=f"{'Drie' if len(bevs)==3 else 'Twee' if len(bevs)==2 else 'Eén'} "
                     f"{'dingen' if len(bevs)>1 else 'ding'} die me opvielen aan het "
                     f"klantcontact van {e(toon)}.",
            n=len(bevs), bevwoord="bevindingen" if len(bevs) > 1 else "bevinding",
            dingwoord="dingen" if len(bevs) > 1 else "ding",
            s1_kop=e(kies(C.S1_KOP.get(km, C.S1_KOP["Het volume groeit sneller dan de bezetting"]), naam)),
            s1_tekst=kies(C.S1_TEKST, naam, 1),
            bevindingen="".join(blokken),
            pivot=e(kantelzin(bevs, fa.get(naam, {}), naam)),
            ask_sub=kies(C.ASK_SUB, naam, 3),
            rekensom_kop=e(kies(C.REKENSOM_KOP, naam, 4)),
            rekensom=kies(C.REKENSOM, naam, 5),
            rekensom_pull=kies(C.REKENSOM_PULL, naam, 6),
            anders=kies(C.ANDERS, naam, 7),
            voorstel_sub=kies(C.VOORSTEL_SUB, naam, 8).format(bedrijf=e(toon)),
            paginaurl=f"{BASISURL}/{s}",
            qr=QR,
            founder1=kies(C.FOUNDER, naam, 9)[0], founder2=kies(C.FOUNDER, naam, 9)[1],
            cta_h=e(kies(C.CTA_H, naam, 10)),
            cta_sub=kies(C.CTA_SUB, naam, 11).format(bedrijf=e(toon)),
            mailonderwerp=e(toon).replace(" ", "%20") + "%20x%20Backbone",
            voornaam=e(voornaam),
            nav_cta=e(kies(C.NAV_CTA, naam, 12)),
            hero_h1=kies(C.HERO_H1, naam, 13),
            slot_tag=e(kies(C.SLOT_TAG, naam, 14)),
            chip_lees=e(kies(C.CHIP_LEES, naam, 15)),
            ask_lees=e(kies(C.ASK_LEES, naam, 16)),
            cta_alt=e(kies(C.CTA_ALT, naam, 17)),
            dock=kies(C.DOCK, naam, 18),
            sheet_note=e(kies(C.SHEET_NOTE, naam, 19)),
            usp_kaarten=usp_blok(naam),
            vinkjes=vinkjes_blok(naam),
        )
        open(os.path.join(UIT, s + ".html"), "w", encoding="utf-8").write(pagina)
        urls.append(f"https://www.{BASISURL}/{s}")
        overzicht.append({"bedrijf": naam, "slug": s, "url": f"https://www.{BASISURL}/{s}",
                          "voornaam": voornaam, "bevindingen": len(bevs),
                          "met_citaat": sum(1 for x in bevs if x["citaat"]),
                          "koopmoment": km})

    # Pagina's opruimen die deze ronde geen bevinding meer opleverden. Zonder dit
    # blijft een oude pagina staan met een claim die inmiddels onjuist is, en dat is
    # erger dan geen pagina.
    houden = {o["slug"] + ".html" for o in overzicht}
    for f in os.listdir(UIT):
        if f.endswith(".html") and f not in houden:
            os.remove(os.path.join(UIT, f))
            print("  verwijderd, claim klopt niet meer:", f)

    with open(os.path.join(BCS, "BCS-Batch4-LP-URLs.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(overzicht[0].keys()))
        w.writeheader(); w.writerows(overzicht)
    open(os.path.join(BCS, "BCS-Batch4-LP-URLs.txt"), "w").write("\n".join(urls) + "\n")

    print(f"{len(overzicht)} pagina's in {UIT}")
    print("  met voornaam op de kaart:", sum(1 for o in overzicht if o["voornaam"]))
    print("  drie bevindingen:", sum(1 for o in overzicht if o["bevindingen"] == 3))
    print("  minstens een letterlijk citaat:", sum(1 for o in overzicht if o["met_citaat"]))
    if zonder:
        print("  zonder bevinding, dus geen pagina:", zonder)


if __name__ == "__main__":
    main()
