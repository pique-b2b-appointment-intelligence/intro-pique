#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bouwt de verzendklare brieven-CSV voor BCS batch 4.

Zeventien kolommen in de canonieke volgorde uit Agents/brieven-csv-agent.md.
De brieftekst bevat geen webadres: sinds 31 augustus 2026 is de QR-code de enige
route. De ondertekening is Jeffrey, want dit is een klantcampagne.
"""
import csv, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
BCS = os.path.dirname(HIER)
sys.path.insert(0, os.environ.get("BCS_OPENINGEN", HIER))
from openingen import OPENING

AFZENDER = "Jeffrey"
BASIS = "https://www.intro-pique.agency"
SLOT = ("Ik ben daarna nog wat dieper in {bedrijf} gedoken. Wat me is opgevallen "
        "staat hiernaast. Scan de QR-code en ik neem je erin mee.")


def persoon(vol):
    """Eerste persoon uit een veld dat er twee kan bevatten, zonder functie ertussen."""
    vol = re.sub(r"\([^)]*\)", " ", vol or "")
    eerste = re.split(r"\s+en\s+|,|/", vol)[0].strip()
    deel = [d for d in eerste.split() if d]
    if not deel or not deel[0][0].isupper() or len(deel[0]) < 3:
        return "", ""
    return deel[0], " ".join(deel[1:])


def adres(a):
    """Splitst op het eerste cijfergroepje: straat, huisnummer, toevoeging."""
    # Het huisnummer is het eerste cijfergroepje dat op witruimte volgt. Zoeken op
    # het eerste cijfer uberhaupt maakte van "2e Tochtweg 98" straat "" met nummer 2.
    m = re.search(r"(?<=\s)\d+", a or "")
    if not m:
        return (a or "").strip(), "", ""
    straat = a[:m.start()].strip().rstrip(",")
    nr = m.group(0)
    rest = a[m.end():].strip().lstrip("-").strip()
    return straat, nr, rest


def pc(p):
    """NL-postcode als 1234 AB, Belgische als vier cijfers."""
    p = re.sub(r"\s+", "", (p or "")).upper()
    return f"{p[:4]} {p[4:]}" if len(p) == 6 else p


def land(p):
    """Vier cijfers zonder letters is een Belgische postcode. Metis Supplements zit
    in Edegem, en een kaart met 'Nederland' eronder komt daar niet aan."""
    return "Belgie" if re.fullmatch(r"\d{4}", re.sub(r"\s+", "", p or "")) else "Nederland"


def main():
    verz = [r for r in csv.DictReader(open(os.path.join(BCS, "BCS-Batch4-Verzendlijst.csv"), encoding="utf-8"))
            if not r["klasse"].startswith("D")]
    urls = {r["bedrijf"]: r for r in csv.DictReader(
        open(os.path.join(BCS, "BCS-Batch4-LP-URLs.csv"), encoding="utf-8"))}
    toon = {r["bedrijf"]: r for r in csv.DictReader(
        open(os.path.join(BCS, "BCS-Batch4-Research-Dossiers.csv"), encoding="utf-8"))}
    sys.path.insert(0, HIER)
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen", os.path.join(HIER, "bcs-lp-generator.py"))
    gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)

    kop = ["voornaam", "achternaam", "aanhef", "straatnaam", "huisnummer", "toevoeging",
           "postcode", "plaatsnaam", "land", "brieftekst", "link", "unieke_url",
           "functie", "bedrijf", "beslisser_bron", "beslisser_status", "notitie"]
    rijen, zonder_naam, vlaggen = [], 0, 0
    for r in sorted(verz, key=lambda x: x["bedrijf"]):
        naam = r["bedrijf"]
        merk = gen.TOONNAAM.get(naam, naam)
        u = urls.get(naam)
        if not u:
            print("  GEEN PAGINA:", naam); continue
        vn, an = persoon(r["naam"])
        straat, nr, toev = adres(r["adres"])
        tekst = OPENING[naam].strip() + "\n\n" + SLOT.format(bedrijf=merk) + "\n\n" + AFZENDER
        notitie = []
        if vn:
            notitie.append(f"Persoonlijk t.a.v. {vn} {an}".strip())
        else:
            zonder_naam += 1
            notitie.append("Brief zonder aanhef, beslisser nog onopgelost")
        if r["adres_oordeel"] != "bevestigd":
            vlaggen += 1
            notitie.append(f"ADRES DUBBELCHECKEN: {r['adres_oordeel'] or 'een bron'}")
        rijen.append({
            "voornaam": vn, "achternaam": an, "aanhef": f"Hoi {vn}" if vn else "",
            "straatnaam": straat, "huisnummer": nr, "toevoeging": toev,
            "postcode": pc(r["postcode"]), "plaatsnaam": r["plaats"], "land": land(r["postcode"]),
            "brieftekst": tekst, "link": u["url"], "unieke_url": "bcs4/" + u["slug"],
            "functie": r["rol"], "bedrijf": merk,
            "beslisser_bron": r["herkomst"],
            "beslisser_status": "GEVERIFIEERD" if r["naam_status"] == "geverifieerd" else "ONOPGELOST",
            "notitie": " | ".join(notitie)})

    uit = os.path.join(BCS, "BCS-Batch4-Brieven-VERZENDKLAAR.csv")
    with open(uit, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=kop, quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(rijen)
    print(f"{len(rijen)} rijen -> {uit}")
    print("  met aanhef:", len(rijen) - zonder_naam, "| zonder aanhef:", zonder_naam)
    print("  adresvlaggen:", vlaggen,
          "| onopgelost:", sum(1 for x in rijen if x["beslisser_status"] == "ONOPGELOST"))


if __name__ == "__main__":
    main()
