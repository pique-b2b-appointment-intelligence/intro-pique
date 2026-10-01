#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cloudpillo via de contentketen, op het oorspronkelijke v2-design.

Dit script vervangt de rotatiegenerator voor precies een pagina. De HTML-vorm
komt ongewijzigd uit bcs-lp-generator.py (Componenten/lp-v2). Alleen de copy is
anders, en die komt uit de keten in plaats van uit zinnenbanken:

  onderzoek  -> servicescan op cloudpillo.com, 1 okt 2026
  factpoort  -> twee scannervondsten afgekeurd:
                  "reactiebelofte binnen 1 uur" was een annuleringstermijn
                  "retourtermijn 30 dagen" is op hun site 100 dagen
  angle      -> bereikbaarheid versus bereik
  rauw       -> scratchpad/bcs5/rauw-cloudpillo.md, 167 woorden, 0 ailint-treffers
  compressie -> onderstaande slots, verplaatst en ingekort, niet verfraaid

Alles wat hieronder tussen aanhalingstekens staat is letterlijk overgetypt van
cloudpillo.com en is daar op 1 oktober 2026 gezien.
"""
import html, importlib.util, io, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
BCS = os.path.dirname(HIER)


def mod(naam, pad):
    spec = importlib.util.spec_from_file_location(naam, pad)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


V4 = mod("v4", os.path.join(HIER, "bcs-lp-generator.py"))
B5 = mod("b5", os.path.join(HIER, "bcs5-lp-generator.py"))
e = html.escape

BEDRIJF, TOON, VOORNAAM = "Cloudpillo", "Cloudpillo", "Lars"
GEZIEN = "1 oktober 2026"

# ── de drie bevindingen, in de volgorde waarin ze gevonden zijn ────────────
BEVINDINGEN = [
    {"kop": "Jullie site staat klaar in elf markten.",
     "tekst": "Duitsland, Oostenrijk, Frankrijk, Spanje, Portugal, het Verenigd "
              "Koninkrijk en nog wat kleinere. Dat zag ik aan de hreflang-regels in "
              "de broncode, niet aan iets dat jullie zelf zeggen.",
     "citaat": "", "dom": "", "datum": ""},
    {"kop": "Er draait Gorgias.",
     "tekst": "Daar betaal je maandelijks voor. Dus die mailbox was op een gegeven "
              "moment te groot om met de hand te doen, en iemand heeft daar bewust "
              "iets voor geregeld.",
     "citaat": "", "dom": "", "datum": ""},
    {"kop": "En de telefoon staat dertig uur per week aan.",
     "tekst": "Dat is wat er op jullie eigen klantenservicepagina staat. Daarnaast "
              "geven jullie honderd dagen retourrecht, dus er kunnen honderd dagen "
              "lang vragen over een bestelling binnenkomen.",
     "citaat": "Bel ons via +31 73 704 4350 Ma-vr 10:00-16:00 uur of stuur ons een "
               "e-mail support@cloudpillo.nl",
     "dom": "cloudpillo.com", "datum": GEZIEN},
]

blokken = []
for i, w in enumerate(BEVINDINGEN):
    bewijs = (V4.BEWIJS_SJABLOON.format(citaat=e(w["citaat"]), dom=e(w["dom"]),
                                        datum=e(w["datum"])) if w["citaat"] else "")
    blokken.append(V4.BEV_SJABLOON.format(
        kant="right" if i % 2 == 0 else "left",
        id=' id="s2"' if i == 0 else "",
        nr="%02d" % (i + 1), tot="%02d" % len(BEVINDINGEN),
        kop=e(w["kop"]), tekst=w["tekst"], bewijs=bewijs))

blokken.append(B5.DRIE_SJABLOON.format(
    kop=e("Drie cijfers die ik niet kan zien."),
    intro=e("Op reactietijd staat bij jullie geen getal. Er staat dat je zo snel "
            "mogelijk terugkomt. Dit is wat ik dan vraag."),
    uit=e("Bijna niemand heeft ze paraat. Dat is ook logisch: het loopt, er piept "
          "niets, dus niemand telt.")))

pagina = V4.SJABLOON.format(
    bedrijf=e(BEDRIJF), bedrijf_js=BEDRIJF,
    terugbel=os.environ.get("BCS_TERUGBEL", ""),
    intro_velden="voornaam: '%s', bedrijf: '%s', " % (VOORNAAM, TOON),
    voornaam=e(VOORNAAM),
    kaart_h="Hoi %s.<br>Ik keek even naar <em>%s</em>." % (e(VOORNAAM), e(TOON)),
    slot_tag=e("De kaart die je vasthield"),

    # [RAUW] de twee dingen die naast elkaar kwamen te liggen
    hero_h1=e("Elf markten, dertig uur."),
    hero_sub=e("Allebei van jullie eigen site. Hieronder staat waar ik keek."),
    n=len(BEVINDINGEN), bevwoord="waarnemingen", dingwoord="dingen",
    chip_lees=e("Twee minuten leeswerk"),

    s1_kop=e("Waarom deze kaart bij jullie ligt."),
    # [RAUW] letterlijk
    s1_tekst=e("Ik ging kijken omdat jullie site in elf markten staat. Daarna bleef "
               "ik hangen bij iets anders."),
    bevindingen="".join(blokken),

    # [RAUW] letterlijk, inclusief de twijfel
    pivot=e("Ik weet niet of dat een probleem is. Misschien vangt Gorgias het prima "
            "op en zijn die dertig uur ruim genoeg. Maar ik kan van buiten niet zien "
            "wat er gebeurt met een mail die zaterdagochtend uit Duitsland binnenkomt."),

    rekensom_kop=e("Wat een dag wachten doet."),
    rekensom="Een klant die op antwoord wacht, bestelt in die dagen niets. Haakt hij "
             "af, dan schrijft hij het soms op. <strong>Die ene regel blijft daarna "
             "staan voor iedereen die jullie opzoekt.</strong>",
    rekensom_pull=e("De duurste vraag is die van de klant die hem twee keer moest stellen."),
    anders=e("Wij meten die drie getallen vanaf dag een. Aan een oplopende reactietijd "
             "zie je twee weken vooruit dat het gaat piepen, en dat is voordat de "
             "eerste klant klaagt."),

    voorstel_sub=e("Een kwartier bellen. Ik reken jullie drie getallen uit en zet ze "
                   "naast de rest van de markt."),
    usp_kaarten=V4.usp_blok(BEDRIJF), vinkjes=V4.vinkjes_blok(BEDRIJF),
    founder1=e("Ik ben Jeffrey. Ik doe het klantcontact voor webshops die harder "
               "groeien dan hun mailbox."),
    # tellscan keurde hier "niet X, maar Y" af. Die constructie staat op de
    # verbodslijst in writing-standards, dus hij is geschrapt in plaats van
    # omgeschreven naar iets dat hetzelfde doet.
    founder2=e("Mensen die in jullie naam en jullie toon antwoorden. Je klant merkt "
               "er niets van dat wij het zijn."),

    cta_h=e("Zal ik je hier even over bellen?"),
    cta_sub=e("Een kwartier, en ik hoef niets voor te bereiden."),
    cta_alt=e("Of laat je nummer achter"),
    ask_sub=e("Vijftien minuten, video of telefoon."),
    ask_lees=e("Ik lees eerst verder"),
    nav_cta=e("Even bellen"), dock=e("Een kwartier plannen"),
    sheet_note=e("Ik bel zelf. Je nummer gaat nergens anders heen."),
    mailonderwerp=e("Klantcontact bij %s" % TOON),
)

# Het sjabloon komt uit batch 4 en zet PQ_CAMPAGNE dus op bcs-batch4. Alle 151
# batch 5-pagina's rapporteren daardoor onder de verkeerde campagne in de
# meting. Hier gerepareerd; voor de rest van de batch is het een aparte ronde.
pagina = re.sub(r"(PQ_CAMPAGNE\s*=\s*)'bcs-batch4'", r"\1'bcs-batch5'", pagina)

doel = os.path.join(BCS, "bcs5", "cloudpillo.html")
io.open(doel, "w", encoding="utf-8").write(pagina)
print("geschreven: %s (%d bytes)" % (doel, len(pagina.encode("utf-8"))))
