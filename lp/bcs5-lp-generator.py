#!/usr/bin/env python3
"""Bouwt de persoonlijke landingspagina's voor BCS batch 5.

De vorm komt uit Componenten/lp-v2 en wordt hier niet aangeraakt. Het paginasjabloon
wordt geleend van de batch 4-generator, zodat er maar een plek is waar de HTML staat.
Dit script levert alleen de inhoud, en die is fundamenteel anders dan in batch 4.

**Wat er verandert en waarom.** Batch 4 opende met een bevinding over de inrichting van
de klantenservice. Dat gaf over vier batches nul afspraken, want die inrichting is een
bewuste keuze en het antwoord is dus altijd "we doen hier al iets mee". Batch 5 zegt
nergens dat er iets mis is. De pagina toont wat er aan volume zichtbaar is en stelt
daarna drie vragen waarop bijna geen webshop het antwoord heeft. Zie
`Klanten/BCS/BCS-Belscript-Batch5-Cijfers.md`.

**Twee regels die hier hard zijn.**

1. Een waarneming zonder letterlijk citaat krijgt geen bewijsblok. Een parafrase tussen
   aanhalingstekens is de duurste fout die er is, want de prospect controleert het in
   dertig seconden op zijn eigen site.
2. Een waarneming is een feit over volume, nooit een oordeel over hun service. "Jullie
   publiceren 18.510 reviews" mag. "Jullie reageren traag" niet, want dat weten we niet.

Gebruik:
    python3 bcs5-lp-generator.py [--uit bcs5]
"""
import argparse, csv, html, importlib.util, os, re, shutil, sys, unicodedata
from datetime import date

HIER = os.path.dirname(os.path.abspath(__file__))
BCS = os.path.dirname(HIER)
SWEEP = os.path.join(HIER, "sweep")
COMP = os.path.abspath(os.path.join(BCS, "..", "..", "Componenten", "lp-v2"))
GECHECKT = "24 september 2026"
BASISURL = os.environ.get("BCS_LP_BASIS", "intro-pique.agency/bcs5")


def mod(naam, pad):
    spec = importlib.util.spec_from_file_location(naam, pad)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


C = mod("bcs5copy", os.path.join(HIER, "bcs5-lp-copy.py"))
# Het paginasjabloon komt uit de batch 4-generator. Die is importeerbaar omdat main()
# achter een __main__-guard staat, dus er draait niets mee.
V4 = mod("bcs4gen", os.path.join(HIER, "bcs-lp-generator.py"))


def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def kies(lijst, sleutel, offset=0):
    """Vaste keuze per bedrijf, zodat een prospect bij herhaald bezoek dezelfde pagina ziet."""
    h = sum((i + 1) * ord(c) for i, c in enumerate(sleutel))
    return lijst[(h + offset) % len(lijst)]


def e(s):
    return html.escape(str(s or ""), quote=True)


def getal(s):
    try:
        return int(re.sub(r"[^\d]", "", str(s or "")) or 0)
    except ValueError:
        return 0


def nl(n):
    """18510 wordt 18.510. Een getal met punten leest als een hoeveelheid, zonder punten
    als een productcode."""
    return f"{n:,}".replace(",", ".")


def toonnaam(s):
    """De naam zoals een mens hem zegt. "123 3D B.V." wordt "123 3D".

    De statutaire vorm hoort niet in een lopende zin, en hij gaf ook een dubbele punt in
    de kop: "Drie getallen over 123 3D B.V.." Wie een B.V. in een aanhef zet, laat zien
    dat hij uit een register heeft gekopieerd."""
    s = re.sub(r"\s*\b(B\.?V\.?|N\.?V\.?|V\.?O\.?F\.?|BVBA|SRL|Holding|Group)\b\.?\s*$", "",
               str(s or "").strip(), flags=re.I)
    return re.sub(r"\s+", " ", s.replace("®", "").replace("™", "")).strip(" .,-") or str(s)


# Een citaat moet een zin zijn. Een platgeslagen menu eindigt ook op een punt en komt
# anders zo op de pagina: "Home Zakelijk bestellen Zakelijk bestellen Of het nu gaat om".
NAVSTART = re.compile(r"^(home|menu|zoeken|inloggen|winkelwagen|ons vacatureaanbod|"
                      r"alle |bekijk |lees meer|overslaan|ga naar|sluiten|filter|sorteer|"
                      r"vorige|volgende|mijn account|klantenservice\s*$)", re.I)


def bruikbaar_citaat(c):
    """Twijfel telt als onbruikbaar. Een waarneming zonder bewijsblok is niet erg, een
    bewijsblok met een menubalk erin is dodelijk."""
    c = re.sub(r"\s+", " ", str(c or "")).strip()
    if not (30 <= len(c) <= 220) or NAVSTART.match(c):
        return ""
    if not c[:1].isupper():
        return ""
    w = c.lower().split()
    # herhaalde woordgroep verraadt een linklijst
    for n in (2, 3):
        groepen = [" ".join(w[i:i + n]) for i in range(len(w) - n + 1)]
        if len(groepen) != len(set(groepen)):
            return ""
    # vier of meer hoofdletterwoorden achter elkaar is een menu
    if re.search(r"(?:\b[A-Z][a-z]+\s+){4,}", c):
        return ""
    # Een citaat dat de waarneming tegenspreekt is erger dan geen citaat. Partydeco's
    # zakelijk-pagina zegt letterlijk dat factureren niet kan, en dat onder een blok over
    # zakelijke verkoop zetten laat zien dat er niemand heeft meegelezen.
    if re.search(r"\b(niet mogelijk|is het niet|kunnen wij niet|helaas niet|geen (?:zakelijke|b2b))\b",
                 c, re.I):
        return ""
    # " ." of "  " verraadt dat er een element is weggeknipt en de zin dus geknipt is
    if " ." in c or "  " in c:
        return ""
    # een hoofdletterwoord midden in de zin na een kleine letter is een doorgelopen kop
    if re.search(r"[a-z]{3}\s+[A-Z][a-z]+\s+[a-z]", c) and len(c.split()) > 14:
        return ""
    # een zin heeft een werkwoord. Zonder deze toets glipt een opsomming van merknamen erdoor.
    if not re.search(r"\b(is|zijn|was|waren|wordt|worden|heeft|hebben|kan|kunnen|"
                     r"moet|moeten|staat|staan|krijg\w*|doen|doet|bied\w*|lever\w*|"
                     r"zoek\w*|beantwoord\w*|reager\w*|help\w*|maak\w*|ga\w*|"
                     r"neem\w*|geef\w*|zit\w*|blijf\w*|word\w*|ben\w*|zie\w*)\b",
                     c, re.I):
        return ""
    return c


# Een reactiebelofte is een tijd plus een woord over antwoorden. Zonder die dubbele eis
# glipt "Ja, dat kan binnen 30 dagen na ontvangst" erdoor, en dat is een retourtermijn.
# Die fout stond in batch 4 op drie kaarten.
BELOFTE = re.compile(
    r"(binnen|maximale?|uiterlijk|binnen\s+maximaal)\b[^.!?]{0,60}?"
    r"\b(minuut|minuten|uur|uren|werkdag\w*|dag|dagen)\b", re.I)
ANTWOORDWOORD = re.compile(r"(reager|reacti|antwoord|beantwoord|terugbel|terug\s*hoor|"
                           r"verwerkingstermijn|contact\s+met\s+je|horen\s+van\s+ons)", re.I)
RETOUR = re.compile(r"(retour|terugstuur|bedenktijd|herroep|ruilen|geld\s+terug|garantie)", re.I)


def is_belofte(c):
    c = str(c or "")
    return bool(BELOFTE.search(c) and ANTWOORDWOORD.search(c) and not RETOUR.search(c))


def kort(s, maxlen=150):
    s = re.sub(r"\s+", " ", str(s or "")).strip().strip("'\"")
    if len(s) <= maxlen:
        return s
    geknipt = s[:maxlen].rsplit(" ", 1)[0]
    return geknipt + "..."


# ── de waarnemingen ───────────────────────────────────────────────
def waarnemingen(naam, sig, rev, al, keur=None, hand=None, extra=None, hand2=None):
    """Feiten over volume, met waar mogelijk een letterlijk citaat van hun eigen site.

    Volgorde is niet willekeurig: het sterkste bewijs van volume staat vooraan, en dat is
    altijd een getal dat zij zelf publiceren."""
    uit = []
    dom = (sig.get("site") or "https://" + al.get("domein", "")).replace("https://", "").replace("http://", "").rstrip("/")

    # 0. een met de hand opgezochte waarneming. Die bestaat alleen voor de shops waar
    # geen enkele scan doorheen kwam, en de bron staat er per regel bij zodat een mens
    # hem kan nalopen. Hij staat vooraan omdat hij specifieker is dan wat een scan vindt.
    if hand:
        uit.append({"kop": hand["kop"], "tekst": hand["tekst"],
                    "citaat": "", "dom": dom, "datum": GECHECKT})
    # Een tweede met de hand opgezochte waarneming, voor de shops waar de scanners er maar
    # een vonden en een kaartopening er twee nodig heeft. Zie sweep/handwaarnemingen2.csv.
    if hand2:
        uit.append({"kop": hand2["kop"], "tekst": hand2["tekst"],
                    "citaat": "", "dom": dom, "datum": GECHECKT})

    # 1. reviewaantal. Het sterkste volumebewijs dat er is, want zij publiceren het zelf.
    aantal = getal(rev.get("reviewaantal_eigen"))
    if aantal >= 250:
        plat = (rev.get("reviewplatform") or "").split("|")[0]
        waar = f" op {plat.capitalize()}" if plat else ""
        uit.append({
            "kop": f"{nl(aantal)} mensen lieten een beoordeling achter",
            "tekst": f"Dat aantal staat op jullie eigen site{waar}. Het zegt niets over de "
                     f"kwaliteit en daar gaat het me ook niet om. Het zegt iets anders: bij "
                     f"dit aantal beoordelingen liggen er duizenden vragen achter die "
                     f"iemand heeft moeten beantwoorden.",
            "citaat": "", "dom": dom, "datum": GECHECKT})

    # 2. markten en talen
    markten = getal(sig.get("markten_hreflang")) or getal(al.get("markten"))
    if markten > 40:
        # Boven de veertig telt de hreflang geen markten meer maar elke combinatie van
        # taal en land. Dat exacte getal op een pagina zetten is vragen om een correctie.
        uit.append({
            "kop": "Jullie site schakelt tussen tientallen landen en talen",
            "tekst": "Dat staat in de hreflang-regels van de broncode. Bij dat bereik komt "
                     "er in meerdere talen post binnen, en de vraag is wie die taal spreekt "
                     "op het moment dat het bericht binnenkomt.",
            "citaat": "", "dom": dom, "datum": GECHECKT})
    elif 2 <= markten <= 40:
        uit.append({
            "kop": f"Jullie site staat klaar in {markten} taalmarkten",
            "tekst": f"Dat is in de broncode te zien aan de hreflang-regels. Elke markt "
                     f"erbij betekent een vertaalde winkel en daarnaast een mailbox waarin "
                     f"iemand in die taal moet kunnen antwoorden.",
            "citaat": "", "dom": dom, "datum": GECHECKT})

    # 3. vacature. Dit is een handeling met een datum, en daarmee het hardste signaal.
    if sig.get("vac_titel"):
        # "Vacature: Medewerker servicedesk" wordt in een lopende zin "een Vacature
        # medewerker servicedesk". Het woord vacature hoort in de kop, niet in de functie.
        functie = re.sub(r"^\s*(vacature|nieuw|open)\s*[:\-]?\s*", "",
                         sig["vac_titel"], flags=re.I).strip(" :-")
        datumzin = ""
        if sig.get("vac_datum"):
            datumzin = f" De vacature staat sinds {sig['vac_datum']} open."
        uit.append({
            "kop": f"Jullie zoeken een {kort(functie, 60)}",
            "tekst": f"Die stond op jullie eigen vacaturepagina.{datumzin} Iemand erbij "
                     f"zetten werkt, tot het volume weer sneller groeit dan de bezetting. "
                     f"Dat is meestal het moment waarop het opnieuw gaat schuiven.",
            "citaat": bruikbaar_citaat(sig.get("vac_citaat2") or kort(sig.get("vac_citaat", ""), 200)),
            "dom": dom, "datum": GECHECKT})

    # 4. ticketsysteem
    tool = (sig.get("ticketsysteem") or "").split("|")[0]
    if tool:
        uit.append({
            "kop": f"Er draait {tool.capitalize()} op jullie site",
            "tekst": f"Daar betaalt iemand maandelijks voor. Dat betekent dat de mailbox al "
                     f"te groot was om met de hand te doen, en dat iemand die beslissing "
                     f"bewust heeft genomen. De vraag is wat er sindsdien met het volume is "
                     f"gebeurd.",
            "citaat": "", "dom": dom, "datum": GECHECKT})

    # 5. zakelijk kanaal naast de webshop
    if sig.get("b2b_citaat"):
        uit.append({
            "kop": "Naast de webshop loopt er zakelijke verkoop",
            "tekst": "Zakelijke klanten stellen andere vragen dan consumenten: over "
                     "levertijden, facturen en staffels. Bij de meeste shops komen die "
                     "twee soorten vragen in dezelfde mailbox terecht, en dan wint de "
                     "consument het op volume en de zakelijke klant op urgentie.",
            "citaat": bruikbaar_citaat(sig.get("b2b_citaat2") or kort(sig.get("b2b_citaat", ""), 200)), "dom": dom,
            "datum": GECHECKT})

    # 6. hun eigen reactiebelofte. Geen oordeel, wel een getal dat zij zelf noemen.
    belofte = next((c for c in (sig.get("service_citaat2"), sig.get("service_citaat"))
                    if is_belofte(c)), "")
    if belofte:
        uit.append({
            "kop": "Jullie beloven zelf een reactietijd",
            "tekst": "Die belofte staat op jullie klantenservicepagina. Een belofte is een "
                     "getal, en daarmee is het meteen het enige stuk van jullie service dat "
                     "een klant kan narekenen. De vraag is of jullie zelf weten hoe vaak "
                     "hij gehaald wordt.",
            "citaat": bruikbaar_citaat(belofte), "dom": dom, "datum": GECHECKT})

    # 7. het keurmerk. Een lid heeft zich vastgelegd op servicenormen en laat zijn
    # klanttevredenheid meten. Dat is hun eigen keuze en hun eigen cijfer.
    if keur:
        cijfer = (keur.get("sterren") or "").replace(".", ",")
        if cijfer:
            uit.append({
                "kop": f"Jullie laten de service meten en staan op een {cijfer}",
                "tekst": "Dat cijfer hangt aan jullie Thuiswinkel Waarborg-lidmaatschap. "
                         "Het betekent dat er al iemand naar de service kijkt en dat er een "
                         "norm is waaraan jullie je hebben verbonden. Wat een cijfer niet "
                         "laat zien is hoe lang een klant op dat antwoord wachtte.",
                "citaat": "", "dom": dom, "datum": GECHECKT})
        else:
            uit.append({
                "kop": "Jullie zijn aangesloten bij het Thuiswinkel Waarborg",
                "tekst": "Dat is een keuze, geen verplichting, en er hangen servicenormen "
                         "aan vast. Het zegt dat klantcontact bij jullie serieus genoeg is "
                         "om je aan een keurmerk te binden. Het zegt niet hoe snel een "
                         "vraag nu wordt opgepakt.",
                "citaat": "", "dom": dom, "datum": GECHECKT})

    # 8. assortiment, alleen als er verder weinig is
    prod = getal(al.get("producten")) or getal(sig.get("v_producten"))
    # LET OP: precies 1000 is geen assortiment maar de leeslimiet van products.json. Vijftien
    # prospects kwamen daarop uit en kregen alle vijftien de zin "zeker 1.000 artikelen",
    # wat op een kaart zowel onwaar precies is als zichtbaar sjabloon. Tien ervan zijn
    # opnieuw gemeten op hun eigen categoriepagina en lagen tussen 1.079 en 11.540.
    gecapt = prod == 1000
    if gecapt:
        prod = 0
    # LET OP: de drie assortimentsbronnen sluiten elkaar uit op de VRAAG of er al een
    # artikelaantal staat, niet op de vraag of er een getal gemeten is. Op "not prod"
    # toetsen blokkeerde de sitemaptelling bij elke shop die er 1 tot 39 teruggaf, want
    # dan is prod waar en is de waarneming toch niet geplaatst.
    assortiment = False
    if prod >= 40 and len(uit) < 4:
        assortiment = True
        uit.append({
            "kop": f"Jullie voeren zeker {nl(prod)} artikelen",
            "tekst": "Dat is het aantal dat de winkel zelf teruggeeft. Hoe breder het "
                     "assortiment, hoe meer vragen over maten, voorraad en verschillen "
                     "tussen varianten. Dat soort vragen gaat zelden over de bestelling "
                     "zelf en bijna altijd over de keuze ervoor.",
            "citaat": "", "dom": dom, "datum": GECHECKT})

    # 9. hetzelfde assortiment, maar geteld in de sitemap in plaats van in products.json.
    # Alleen voor de shops die niet op Shopify draaien, want daar geeft de winkel zelf geen
    # aantal terug. Zie Context/tools/sitemaptel.py voor wat er wel en niet meegeteld wordt.
    smprod = getal((extra or {}).get("sm_prod"))
    if not assortiment and smprod >= 40 and len(uit) < 4 and smprod != prod:
        assortiment = True
        uit.append({
            "kop": f"Jullie voeren zeker {nl(smprod)} artikelen",
            "tekst": "Zoveel productpagina's staan er in jullie eigen sitemap. Hoe breder "
                     "het assortiment, hoe meer vragen over maten, voorraad en verschillen "
                     "tussen varianten. Dat soort vragen gaat zelden over de bestelling "
                     "zelf en bijna altijd over de keuze ervoor.",
            "citaat": "", "dom": dom, "datum": GECHECKT})

    # 10. het assortiment zoals het winkelplatform het zelf afdrukt. Dit is sterker dan
    # elke eigen telling, want het getal komt uit hun database en staat er letterlijk.
    # Alleen de regels die met de hand gekeurd zijn, zie sweep/assortiment-gekeurd.csv.
    asn = getal((extra or {}).get("as_aantal"))
    if not assortiment and asn >= 40 and len(uit) < 4:
        assortiment = True
        uit.append({
            "kop": f"Jullie voeren zeker {nl(asn)} artikelen",
            "tekst": "Dat aantal drukt jullie eigen winkel af boven de categorie. Hoe breder "
                     "het assortiment, hoe meer vragen over maten, voorraad en verschillen "
                     "tussen varianten. Dat soort vragen gaat zelden over de bestelling "
                     "zelf en bijna altijd over de keuze ervoor.",
            "citaat": "", "dom": dom, "datum": GECHECKT})

    # 11. het aantal ingangen. Elk kanaal is een postvak dat iemand moet legen, en drie of
    # meer aanbieden is een keuze die iets zegt over het aantal vragen. Een kanaal telt
    # alleen bij een hard spoor: een tel-link, een mailto of het assetpad van de widget.
    if gecapt and not assortiment and len(uit) < 4:
        assortiment = True
        uit.append({
            "kop": "Jullie voeren meer dan duizend artikelen",
            "tekst": "Zover kon ik tellen voordat de winkel ophield met doorgeven. Hoe "
                     "breder het assortiment, hoe meer vragen over maten, voorraad en "
                     "verschillen tussen varianten. Dat soort vragen gaat zelden over de "
                     "bestelling zelf en bijna altijd over de keuze ervoor.",
            "citaat": "", "dom": dom, "datum": GECHECKT})

    kan = getal((extra or {}).get("kanalen"))
    lijst = [x for x in ((extra or {}).get("k_lijst") or "").split("|") if x]
    if kan >= 3 and lijst and len(uit) < 4:
        opsom = ", ".join(lijst[:-1]) + " en " + lijst[-1]
        uit.append({
            "kop": f"Er zijn {nl(kan)} manieren om jullie een vraag te stellen",
            "tekst": f"Op jullie eigen pagina's staan {opsom}. Elk kanaal erbij is een "
                     f"postvak dat iemand moet legen, en ze lopen zelden even snel leeg. "
                     f"Bij de meeste shops is er een kanaal waar het blijft liggen, en dat "
                     f"is bijna nooit het kanaal waar het hardst op gelet wordt.",
            "citaat": "", "dom": dom, "datum": GECHECKT,
            "kanalen_lijst": "|".join(lijst)})

    return uit[:4]


DRIE_SJABLOON = """
  <section class="chapter center" id="drie">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">De drie vragen</div>
        <h2 class="ch-kop">{kop}</h2>
        <p class="ch-text">{intro}</p>
        <p class="ch-text"><strong>1.</strong> Hoe lang duurt het nu gemiddeld voordat een klant antwoord heeft?</p>
        <p class="ch-text"><strong>2.</strong> Wat vinden jullie klanten van de service, uitgedrukt in een cijfer?</p>
        <p class="ch-text"><strong>3.</strong> Hoeveel procent is in een bericht opgelost, zonder heen en weer?</p>
        <p class="ch-text">{uit}</p>
      </div>
    </div>
  </section>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--uit", default="bcs5")
    p.add_argument("--lijst", default=os.path.join(SWEEP, "BCS-Batch5-DEFINITIEF-151.csv"))
    a = p.parse_args()
    UIT = os.path.join(BCS, a.uit)

    def lees(pad, sleutel="bedrijf"):
        if not os.path.exists(pad):
            print(f"  let op: {pad} ontbreekt", file=sys.stderr)
            return {}
        return {r[sleutel]: r for r in csv.DictReader(open(pad, encoding="utf-8"))}

    prospects = list(csv.DictReader(open(a.lijst, encoding="utf-8")))
    # def151-citaten.csv is def151-signalen.csv met de blok-citaten erbij (citaatoogst.py)
    citpad = os.path.join(SWEEP, "def151-citaten.csv")
    sig = lees(citpad if os.path.exists(citpad) else os.path.join(SWEEP, "def151-signalen.csv"))
    rev = lees(os.path.join(SWEEP, "def151-reviews.csv"))
    al = lees(os.path.join(SWEEP, "BATCH5-A-LIJST.csv"))
    hand = lees(os.path.join(SWEEP, "handwaarnemingen.csv"))
    # Bijgevangen feiten voor de shops waar de eerste ronde maar één ding vond: het
    # artikelaantal uit de sitemap en het aantal contactkanalen. Zie Context/tools/sitemaptel.py
    # en Context/tools/kanalen.py.
    extra = lees(os.path.join(SWEEP, "extra-feiten.csv"))
    hand2 = lees(os.path.join(SWEEP, "handwaarnemingen2.csv"))
    # De ledenpagina van Thuiswinkel geeft ook het keurmerkcijfer. Dat is een getal dat
    # zij zelf hebben laten meten, dus het mag geciteerd worden zonder oordeel.
    tw = {}
    for r in csv.DictReader(open(os.path.join(SWEEP, "tw-detail.csv"), encoding="utf-8")) \
            if os.path.exists(os.path.join(SWEEP, "tw-detail.csv")) else []:
        d = (r.get("domein") or "").lower().replace("www.", "").strip("/")
        if d:
            tw[d] = r

    os.makedirs(UIT, exist_ok=True)
    for f in ("lp.css", "lp-v2.js", "lp-intro.js"):
        shutil.copy(os.path.join(COMP, f), UIT)
    for f in ("thema-bcs.css", "jeffrey-staand.mp4", "jeffrey-staand-poster.jpg",
              "jeffrey-dylan.jpg", "jeffrey-avatar.jpg",
              "bcs-logo.png", "bcs-logo-licht.png", "favicon.png"):
        bron = os.path.join(HIER, f)
        if os.path.exists(bron):
            shutil.copy(bron, UIT)
        else:
            shutil.copy(os.path.join(COMP, os.path.basename(f)), UIT)

    urls, zonder = [], []
    for r in prospects:
        naam = r["bedrijf"]
        toon = toonnaam(naam)
        s = slug(naam)
        wn = waarnemingen(naam, sig.get(naam, {}), rev.get(naam, {}), al.get(naam, {}),
                          tw.get((r["domein"] or "").lower()), hand.get(naam),
                          extra.get(naam), hand2.get(naam))
        # Eén waarneming is genoeg voor een pagina. De waarnemingen zijn in batch 5 niet
        # het punt: ze laten zien dat er naar dit bedrijf gekeken is, en de drie vragen
        # dragen de pagina. Nul waarnemingen is wel een reden om niets te sturen.
        if not wn:
            zonder.append(naam)
            continue

        voornaam = ""
        vol = (r.get("beslisser") or "").strip()
        if vol:
            deel = re.split(r"\s+en\s+|,|/", vol)[0].strip().split()
            if deel and deel[0][:1].isupper() and len(deel[0]) > 2:
                voornaam = deel[0]

        blokken = []
        for i, w in enumerate(wn):
            bewijs = ""
            if w["citaat"]:
                bewijs = V4.BEWIJS_SJABLOON.format(citaat=e(w["citaat"]), dom=e(w["dom"]),
                                                   datum=e(w["datum"]))
            blokken.append(V4.BEV_SJABLOON.format(
                kant="right" if i % 2 == 0 else "left",
                id=' id="s2"' if i == 0 else "",
                nr=f"{i+1:02d}", tot=f"{len(wn):02d}",
                kop=e(w["kop"]), tekst=w["tekst"], bewijs=bewijs))
        blokken.append(DRIE_SJABLOON.format(
            kop=e(kies(C.DRIE_KOP, naam)),
            intro=e(kies(C.DRIE_IN, naam).format(bedrijf=toon)),
            uit=e(kies(C.DRIE_UIT, naam))))

        kaart_h = (f"Hoi {e(voornaam)}.<br>Ik keek even naar <em>{e(toon)}</em>."
                   if voornaam else f"Ik keek even<br>naar <em>{e(toon)}</em>.")
        intro_velden = (f"voornaam: '{e(voornaam)}', bedrijf: '{e(toon)}', "
                        if voornaam else f"bedrijf: '{e(toon)}', ")

        pagina = V4.SJABLOON.format(
            bedrijf=e(naam), bedrijf_js=naam.replace("'", "\\'"),
            terugbel=os.environ.get("BCS_TERUGBEL", ""),
            intro_velden=intro_velden, voornaam=e(voornaam),
            kaart_h=kaart_h, slot_tag=e(kies(C.SLOT_TAG, naam)),
            hero_h1=f"Drie getallen over {e(toon)}.",
            hero_sub=e(kies(C.HERO_SUB, naam)),
            n=len(wn), bevwoord="waarnemingen" if len(wn) != 1 else "waarneming",
            dingwoord="dingen" if len(wn) != 1 else "ding",
            chip_lees=e(kies(C.CHIP_LEES, naam)),
            s1_kop=e(kies(C.S1_KOP, naam).format(bedrijf=toon)),
            s1_tekst=e(kies(C.S1_STAART, naam)),
            bevindingen="".join(blokken),
            pivot=e(kies(C.PIVOT, naam)),
            rekensom_kop=e(kies(C.KOST_KOP, naam)),
            rekensom=kies(C.KOST, naam),
            rekensom_pull=e(kies(C.KOST_PULL, naam)),
            anders=e(kies(C.ANDERS, naam)),
            voorstel_sub=e(kies(C.VOORSTEL_SUB, naam).format(bedrijf=toon)),
            usp_kaarten=V4.usp_blok(naam), vinkjes=V4.vinkjes_blok(naam),
            founder1=e(kies(C.FOUNDER, naam)[0]), founder2=e(kies(C.FOUNDER, naam)[1]),
            cta_h=e(kies(C.CTA_H, naam)),
            cta_sub=e(kies(C.CTA_SUB, naam).format(bedrijf=toon)),
            cta_alt=e(kies(C.CTA_ALT, naam)),
            ask_sub=e(kies(C.ASK_SUB, naam)), ask_lees=e(kies(C.ASK_LEES, naam)),
            nav_cta=e(kies(C.NAV_CTA, naam)), dock=e(kies(C.DOCK, naam)),
            sheet_note=e(kies(C.SHEET_NOTE, naam)),
            mailonderwerp=e(f"Klantcontact bij {toon}"),
        )
        # Het sjabloon komt uit batch 4 en zegt daar "20 minuten". Batch 5 vraagt een
        # kwartier, en die twee door elkaar op een pagina leest als slordigheid. Het
        # sjabloon zelf blijft ongemoeid, want er hangen 88 batch 4-pagina's aan.
        pagina = pagina.replace("20 minuten met Jeffrey", "Een kwartier met Jeffrey")
        open(os.path.join(UIT, f"{s}.html"), "w", encoding="utf-8").write(pagina)
        urls.append({"bedrijf": naam, "domein": r["domein"], "slug": s,
                     "url": f"https://{BASISURL}/{s}", "waarnemingen": len(wn),
                     "beslisser": r.get("beslisser", ""), "voornaam": voornaam})

    with open(os.path.join(BCS, "BCS-Batch5-LP-URLs.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(urls[0].keys())); w.writeheader(); w.writerows(urls)
    print(f"{len(urls)} pagina's -> {UIT}")
    print(f"  met aanhef (voornaam bekend): {sum(1 for u in urls if u['voornaam'])}")
    import collections
    print("  waarnemingen per pagina:", dict(sorted(collections.Counter(u["waarnemingen"] for u in urls).items())))
    if zonder:
        print(f"  te weinig waarnemingen, geen pagina ({len(zonder)}): {zonder[:12]}")


if __name__ == "__main__":
    main()
