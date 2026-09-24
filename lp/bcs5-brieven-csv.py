#!/usr/bin/env python3
"""Bouwt de verzendklare brieven-CSV voor BCS batch 5.

Vier regels die hier hard zijn, elk uit een eerdere fout:

1. **Twee controleerbare feiten die botsen.** De opening is nooit een feit plus een
   uitspraak over hun naam, merk of uitstraling. De toets: kan de prospect de tweede zin
   in dertig seconden op zijn eigen site nakijken. Zo nee, herschrijven.
2. **Geen webadres in de brieftekst.** Per 31 augustus 2026. De slotzin verwijst naar de
   QR-code, niet naar een URL.
3. **Ondertekenen met alleen de voornaam.** Geen "Groet," ervoor.
4. **De kaart en de pagina moeten kloppen.** Het eerste feit op de kaart is dezelfde
   waarneming als bevinding 01 op de landingspagina. Herschrijf je de een, controleer dan
   de ander.

De feiten komen uit dezelfde functie die de landingspagina vult, zodat ze per definitie
overeenkomen. Zie bcs5-lp-generator.py.

Gebruik:
    python3 bcs5-brieven-csv.py
"""
import csv, importlib.util, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
BCS = os.path.dirname(HIER)
SWEEP = os.path.join(HIER, "sweep")
BASISURL = os.environ.get("BCS_LP_BASIS", "intro-pique.agency/bcs5")


def mod(naam, pad):
    spec = importlib.util.spec_from_file_location(naam, pad)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


G = mod("bcs5gen", os.path.join(HIER, "bcs5-lp-generator.py"))
C = mod("bcs5copy", os.path.join(HIER, "bcs5-lp-copy.py"))


def lees(pad, sleutel="bedrijf"):
    if not os.path.exists(pad):
        return {}
    return {r[sleutel]: r for r in csv.DictReader(open(pad, encoding="utf-8"))}


def kaartzin(w, toon):
    """Van een waarneming naar een zin die op karton past.

    De kop op de pagina is een kop en leest op een kaart als een slogan. Hier staat de
    zin die een mens zou schrijven."""
    k = w["kop"]
    m = re.match(r"^([\d.]+) mensen lieten een beoordeling achter$", k)
    if m:
        return f"Op jullie site staan {m.group(1)} beoordelingen."
    m = re.match(r"^Jullie site staat klaar in (\d+) taalmarkten$", k)
    if m:
        return f"Jullie webshop draait in {m.group(1)} taal- en marktvarianten."
    if k.startswith("Jullie site schakelt tussen"):
        return "Jullie webshop schakelt tussen tientallen landen en talen."
    m = re.match(r"^Jullie zoeken een (.+)$", k)
    if m:
        return f"Jullie zoeken een {m.group(1)[0].lower() + m.group(1)[1:]}."
    m = re.match(r"^Er draait (.+) op jullie site$", k)
    if m:
        return f"Er draait {m.group(1)} op jullie site."
    if k.startswith("Naast de webshop loopt"):
        return "Naast de webshop verkopen jullie ook zakelijk."
    if k.startswith("Jullie beloven zelf"):
        c = (w.get("citaat") or "").strip().rstrip(".")
        return f"Op jullie servicepagina staat: {c[0].lower() + c[1:]}." if c else \
               "Op jullie servicepagina staat een reactietijd."
    m = re.match(r"^Jullie laten de service meten en staan op een (.+)$", k)
    if m:
        return f"Jullie laten de service meten en staan op een {m.group(1)}."
    if k.startswith("Jullie zijn aangesloten"):
        return "Jullie zijn aangesloten bij het Thuiswinkel Waarborg."
    if k == "Jullie voeren meer dan duizend artikelen":
        return "In de webshop erachter staan meer dan duizend artikelen."
    m = re.match(r"^Jullie voeren zeker ([\d.]+) artikelen$", k)
    if m:
        return f"In de webshop erachter staan {m.group(1)} artikelen."
    m = re.match(r"^Er zijn (\S+) manieren om jullie een vraag te stellen$", k)
    if m:
        lijst = [x for x in (w.get("kanalen_lijst") or "").split("|") if x]
        opsom = ", ".join(lijst[:-1]) + " en " + lijst[-1] if len(lijst) > 1 else ""
        return (f"Jullie zijn op {m.group(1)} manieren te bereiken: {opsom}."
                if opsom else f"Jullie zijn op {m.group(1)} manieren te bereiken.")
    # een met de hand opgezochte waarneming: de kop is al een zin zonder punt
    return k.rstrip(".") + "."


def main():
    prospects = list(csv.DictReader(
        open(os.path.join(SWEEP, "BCS-Batch5-DEFINITIEF-151.csv"), encoding="utf-8")))
    citpad = os.path.join(SWEEP, "def151-citaten.csv")
    sig = lees(citpad if os.path.exists(citpad) else os.path.join(SWEEP, "def151-signalen.csv"))
    rev = lees(os.path.join(SWEEP, "def151-reviews.csv"))
    al = lees(os.path.join(SWEEP, "BATCH5-A-LIJST.csv"))
    hand = lees(os.path.join(SWEEP, "handwaarnemingen.csv"))
    extra = lees(os.path.join(SWEEP, "extra-feiten.csv"))
    hand2 = lees(os.path.join(SWEEP, "handwaarnemingen2.csv"))
    # Dubbelpoort. Een prospect die van een andere Pique-klant al een handgeschreven kaart
    # kreeg met een QR naar hetzelfde domein, ziet bij de tweede kaart het mechanisme.
    # SCHRAPPEN valt uit de verzendlijst, de rest krijgt een waarschuwing mee.
    dubbel = lees(os.path.join(BCS, "BCS-Batch5-Dubbelcheck.csv"))
    # De beslisserstand komt uit de beslisserlijst en staat hier niet hardgecodeerd. Stond
    # er eerst wel, en dat is gevaarlijk: de kolom bleef GEVERIFIEERD roepen ongeacht wat
    # er in A-BESLISSERS.csv veranderde.
    bes = {}
    bpad = os.path.join(SWEEP, "A-BESLISSERS.csv")
    if os.path.exists(bpad):
        for b in csv.DictReader(open(bpad, encoding="utf-8")):
            d = (b.get("domein") or "").lower().replace("www.", "").strip("/")
            if d:
                bes[d] = b
    tw = {}
    twpad = os.path.join(SWEEP, "tw-detail.csv")
    if os.path.exists(twpad):
        for r in csv.DictReader(open(twpad, encoding="utf-8")):
            d = (r.get("domein") or "").lower().replace("www.", "").strip("/")
            if d:
                tw[d] = r

    uit, zonder, geschrapt = [], [], []
    for r in prospects:
        naam = r["bedrijf"]
        toon = G.toonnaam(naam)
        # Dezelfde functie die de pagina vult, maar zonder de grens van vier, want op de
        # kaart mag een feit staan dat op de pagina niet meer paste.
        wn = G.waarnemingen(naam, sig.get(naam, {}), rev.get(naam, {}), al.get(naam, {}),
                            tw.get((r["domein"] or "").lower()), hand.get(naam),
                            extra.get(naam), hand2.get(naam))
        if len(wn) < 2:
            zonder.append(naam)
            continue

        d = dubbel.get(naam)
        if d and d["advies"] == "SCHRAPPEN":
            geschrapt.append((naam, d["eerdere_batch"]))
            continue

        vol = (r.get("beslisser") or "").strip()
        deel = re.split(r"\s+en\s+|,|/", vol)[0].strip().split()
        voornaam = deel[0] if deel and deel[0][:1].isupper() and len(deel[0]) > 2 else ""
        achternaam = " ".join(deel[1:]) if len(deel) > 1 else ""

        feit1, feit2 = kaartzin(wn[0], toon), kaartzin(wn[1], toon)
        midden = G.kies(C.KAART_MIDDEN, naam).format(bedrijf=toon)
        tekst = f"{feit1} {feit2}\n\n{midden}\n\nJeffrey"

        pc = (r.get("postcode") or "").replace(" ", "")
        pcnet = f"{pc[:4]} {pc[4:]}" if len(pc) == 6 and pc[4:].isalpha() else pc
        hn = (r.get("huisnummer") or "").strip()
        m = re.match(r"^(\d+)\s*([A-Za-z].*)?$", hn)
        nummer, toevoeging = (m.group(1), (m.group(2) or "").strip()) if m else (hn, "")

        notitie = []
        if d:
            notitie.append(f"{d['advies']}: kreeg al een kaart via {d['eerdere_batch']}")
        if not voornaam:
            notitie.append("GEEN AANHEF: beslisser niet op voornaam te noemen")
        if "LET OP" in (r.get("adres_gecontroleerd") or ""):
            notitie.append(r["adres_gecontroleerd"])
        elif "gecorrigeerd" in (r.get("adres_gecontroleerd") or ""):
            notitie.append("adres in de officiele BAG-schrijfwijze gezet")
        if r.get("land") == "Belgie":
            notitie.append("Belgisch adres, niet door de BAG getoetst")

        uit.append({
            "voornaam": voornaam, "achternaam": achternaam,
            "aanhef": f"Hoi {voornaam}" if voornaam else "",
            "straatnaam": r.get("straat", ""), "huisnummer": nummer, "toevoeging": toevoeging,
            "postcode": pcnet, "plaatsnaam": r.get("plaats", ""), "land": r.get("land", "Nederland"),
            "brieftekst": tekst,
            "link": f"https://{BASISURL}/{G.slug(naam)}",
            "unieke_url": f"bcs5/{G.slug(naam)}",
            "functie": r.get("rol", ""), "bedrijf": toon,
            "beslisser_bron": r.get("beslisser_bron", ""),
            "beslisser_status": (bes.get((r["domein"] or "").lower().replace("www.", "")
                                         .strip("/"), {}).get("status") or "ONBEKEND").strip(),
            "notitie": " | ".join(notitie),
        })

    pad = os.path.join(BCS, "BCS-Batch5-Brieven-VERZENDKLAAR.csv")
    with open(pad, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(uit[0].keys()), quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(uit)
    print(f"{len(uit)} brieven -> {pad}")
    print(f"  met aanhef            : {sum(1 for x in uit if x['aanhef'])}")
    print(f"  Nederland / Belgie    : {sum(1 for x in uit if x['land']=='Nederland')} / "
          f"{sum(1 for x in uit if x['land']=='Belgie')}")
    print(f"  met een notitie       : {sum(1 for x in uit if x['notitie'])}")
    lengtes = [len(x["brieftekst"].split()) for x in uit]
    print(f"  woorden per kaart     : {min(lengtes)} tot {max(lengtes)}, "
          f"gemiddeld {sum(lengtes)//len(lengtes)}")
    if geschrapt:
        print(f"  uit de lijst gehaald als dubbele ({len(geschrapt)}):")
        for n, w in geschrapt: print(f"     {n} - kreeg al een kaart via {w}")
    if zonder:
        print(f"  te weinig feiten voor een opening ({len(zonder)}): {zonder[:10]}")

    # De brieven los wegschrijven, want tellscan leest bestanden en geen CSV-kolom.
    # Als .md, want tellscan pakt in een map alleen *.html en *.md op en loopt stil met
    # "geen bestanden gevonden" over een map vol .txt.
    losmap = os.path.join(SWEEP, "brieven5-los")
    os.makedirs(losmap, exist_ok=True)
    for oud in os.listdir(losmap):
        os.remove(os.path.join(losmap, oud))
    for x in uit:
        open(os.path.join(losmap, G.slug(x["bedrijf"]) + ".md"), "w",
             encoding="utf-8").write(x["brieftekst"])
    print(f"  los weggeschreven voor tellscan -> {losmap}")


if __name__ == "__main__":
    main()
