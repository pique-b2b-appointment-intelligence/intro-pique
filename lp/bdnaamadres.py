#!/usr/bin/env python3
"""Haalt in een ronde naam en adres op bij Bedrijfsdata. Twee credits per bedrijf.

Dit is de omgekeerde volgorde ten opzichte van hoe batch 4 gebouwd is, en dat is de les:
eerst kijken of er uberhaupt een naam en een postadres bestaan, en pas daarna tijd steken
in volumebewijs en research. Een prospect waar je geen kaart heen kunt sturen, hoef je
niet te onderzoeken.

De resultaten staan onder de sleutel 'companies' of 'people', niet onder 'data'. Dat is
een valkuil die een hele batchronde kan kosten.

Namen uit de vaste terugvalset gooit dit script weg. Bedrijfsdata geeft die terug wanneer
hij geen personen kent bij een domein, en ze duiken dan bij tientallen bedrijven op.

Gebruik:
    python3 bdnaamadres.py <in.csv> <uit.csv>
"""
import csv, json, re, ssl, sys, urllib.parse, urllib.request
from pathlib import Path

CTX = ssl.create_default_context()
FALLBACK = {"koen avest", "brego keller", "christina groen", "marc oudewortel"}
RANG = [(re.compile(r"(?i)\b(eigenaar|owner|oprichter|founder|co-?founder|dga)\b"), 5),
        (re.compile(r"(?i)\b(ceo|directeur|director|bestuurder|managing|zaakvoerder)\b"), 5),
        (re.compile(r"(?i)\b(coo|operations?|operationeel)\b"), 4),
        (re.compile(r"(?i)\b(e-?commerce|online|webshop)\b"), 4),
        (re.compile(r"(?i)\b(manager|hoofd|lead)\b"), 2)]
NIET = re.compile(r"(?i)assistent|medewerk|stagiair|receptie|administrat|magazijn|"
                  r"logistic|warehouse|intern\b|developer|designer")


def sleutel():
    for r in (Path.home() / ".pique" / "bedrijfsdata.env").read_text().splitlines():
        if r.strip().startswith("BD_API_KEY"):
            return r.split("=", 1)[1].strip().strip("\"'")
    sys.exit("geen sleutel")


def rijen(d):
    for k in ("companies", "people", "data", "results", "items"):
        if isinstance(d.get(k), list):
            return d[k]
    return []


def call(pad, params, key):
    q = urllib.parse.urlencode(dict(params, api_key=key))
    try:
        with urllib.request.urlopen(f"https://api.bedrijfsdata.nl/v1.3/{pad}?{q}",
                                    timeout=35, context=CTX) as f:
            return json.loads(f.read())
    except Exception:
        return {}


def bruikbaar(naam):
    """Een voornaam die je op een kaart kunt schrijven. Initialen vallen af."""
    d = (naam or "").split()
    return bool(d) and len(d[0].strip(".")) >= 3 and not re.fullmatch(r"(?:[A-Z]\.?){1,4}", d[0])


def main():
    key = sleutel()
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    uit = []
    for i, r in enumerate(rows, 1):
        n, dom = r["bedrijf"], (r.get("domein") or r.get("website") or "").strip()
        o = {"bedrijf": n, "domein": dom, "vertical": r.get("vertical", ""),
             "naam": "", "rol": "", "adres": "", "postcode": "", "plaats": "", "kvk": ""}
        d = call("companies", {"domain": dom, "limit": 1} if dom else {"name": n, "limit": 1}, key)
        c = (rijen(d) or [None])[0]
        if c:
            o.update(adres=c.get("address", ""), postcode=c.get("postcode", ""),
                     plaats=c.get("city", ""), kvk=str(c.get("coc") or ""))
        d = call("people", {"name": n, "domain": dom, "limit": 25} if dom else {"name": n, "limit": 25}, key)
        kand = []
        for m in rijen(d):
            vol = (m.get("name") or "").strip()
            rol = (m.get("job_title") or "").strip()
            if not vol or vol.lower() in FALLBACK or NIET.search(rol) or not bruikbaar(vol):
                continue
            s = next((s for p, s in RANG if p.search(rol)), 0)
            if s:
                kand.append((s, vol, rol))
        if kand:
            kand.sort(key=lambda x: -x[0])
            o["naam"], o["rol"] = kand[0][1], kand[0][2]
        uit.append(o)
        v = "NAAM+ADRES" if o["naam"] and o["adres"] else ("adres" if o["adres"] else "-")
        print(f"  {i:>3}/{len(rows)} {n[:22]:<22} {v:<11} {o['naam'][:22]:<22} {o['plaats'][:16]}", flush=True)
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(uit[0].keys()))
        w.writeheader(); w.writerows(uit)
    beide = sum(1 for x in uit if x["naam"] and x["adres"])
    print(f"\nnaam EN adres: {beide} | alleen adres: {sum(1 for x in uit if x['adres'] and not x['naam'])} | van {len(uit)}")
    print("saldo:", call("companies", {"domain": "wolplein.nl", "limit": 1}, key).get("credits_used_month"), "van 5000")


if __name__ == "__main__":
    main()
