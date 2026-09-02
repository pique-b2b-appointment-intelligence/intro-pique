#!/usr/bin/env python3
"""Haalt het postadres op via Bedrijfsdata /companies. Een credit per bedrijf.

Waarom dit endpoint: het geeft straat met huisnummer, postcode, plaats, KVK-nummer
en een BAG-adres-id in een keer. Dat BAG-id betekent dat het adres bestaat, dus de
losse controle met bagcheck.py kan ervoor vervallen.

Wat het NIET zegt is of het bedrijf er ook echt zit. Dat blijft de tweede bron, en
daarvoor kijken we of hetzelfde adres op hun eigen site staat.

Gebruik:
    python3 adressen.py <in.csv met kolom bedrijf en domein> <uit.csv>
"""
import csv, json, os, ssl, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path

BASIS = "https://api.bedrijfsdata.nl/v1.3"
CTX = ssl.create_default_context()


def sleutel():
    k = os.environ.get("BD_API_KEY", "").strip()
    if k:
        return k
    for r in (Path.home() / ".pique" / "bedrijfsdata.env").read_text().splitlines():
        if r.strip().startswith("BD_API_KEY"):
            return r.split("=", 1)[1].strip().strip("\"'")
    sys.exit("geen sleutel")


def main():
    key = sleutel()
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    uit, credits = [], 0
    for i, r in enumerate(rows, 1):
        dom = (r.get("domein") or r.get("website") or "").strip()
        o = {"bedrijf": r["bedrijf"], "domein": dom, "statutaire_naam": "", "adres": "",
             "postcode": "", "plaats": "", "kvk": "", "bag_id": "", "notitie": ""}
        if not dom:
            o["notitie"] = "geen domein"; uit.append(o); continue
        q = urllib.parse.urlencode({"domain": dom, "limit": 1, "api_key": key})
        try:
            with urllib.request.urlopen(f"{BASIS}/companies?{q}", timeout=35, context=CTX) as f:
                d = json.loads(f.read())
        except urllib.error.HTTPError as e:
            o["notitie"] = f"http {e.code}"; uit.append(o); continue
        except Exception as e:
            o["notitie"] = str(e)[:50]; uit.append(o); continue
        credits += d.get("credits_used", 0) or 0
        c = (d.get("data") or d.get("companies") or [None])[0]
        if not c:
            o["notitie"] = "bedrijf niet gevonden"; uit.append(o); continue
        o.update(statutaire_naam=c.get("name", ""), adres=c.get("address", ""),
                 postcode=c.get("postcode", ""), plaats=c.get("city", ""),
                 kvk=str(c.get("coc") or ""), bag_id=c.get("bag_addressid", ""))
        if not o["adres"]:
            o["notitie"] = "geen adres in het antwoord"
        uit.append(o)
        print(f"  {i:>2}/{len(rows)} {r['bedrijf'][:22]:<22} {o['adres'][:28]:<28} "
              f"{o['postcode']:<8} {o['plaats'][:18]}", flush=True)
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(uit[0].keys()))
        w.writeheader(); w.writerows(uit)
    vol = sum(1 for r in uit if r["adres"] and r["postcode"] and r["plaats"])
    print(f"\nvolledig adres: {vol} van {len(uit)}   credits: {credits}")


if __name__ == "__main__":
    main()
