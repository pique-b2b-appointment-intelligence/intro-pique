#!/usr/bin/env python3
"""Zoekt de beslisser eerst op de site van het bedrijf zelf. Kost geen credits.

Waarom eerst hier: een bedrijf dat zijn oprichter op de over-ons-pagina zet, is de
sterkste en goedkoopste bron die er is. Pas wat hier niets oplevert, gaat door naar
de betaalde route.

Wat eruit komt zijn KANDIDATEN. De beslisser-poort vraagt twee onafhankelijke bronnen
waarvan een jonger dan 90 dagen, dus een naam van hier gaat nooit zonder tweede bron
een brief in.

Gebruik:
    python3 beslisser-gratis.py beslissers-open.csv beslissers-gratis.csv
"""
import csv, os, re, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings("ignore")
import requests
requests.packages.urllib3.disable_warnings()

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "Context", "tools")))
from signaalscan import tekst, namen  # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
H = {"User-Agent": UA, "Accept-Language": "nl-NL,nl;q=0.9"}
PADEN = ["/pages/over-ons", "/over-ons", "/pages/about", "/about", "/about-us",
         "/pages/ons-verhaal", "/ons-verhaal", "/pages/team", "/team",
         "/pages/wie-zijn-wij", "/pages/our-story", "/our-story", "/pages/about-us",
         "/verhaal", "/pages/contact", "/contact"]


def haal(basis, pad):
    for poging in range(2):
        try:
            r = requests.get(basis + pad, headers=H, timeout=18, verify=False)
        except Exception:
            return ""
        if r.status_code == 429:
            time.sleep(5 + 5 * poging)
            continue
        if r.status_code == 200 and len(r.text) > 1200:
            return r.text
        return ""
    return ""


def scan(row):
    dom = row["domein"].strip()
    uit = {"bedrijf": row["bedrijf"], "domein": dom, "kandidaten": "", "bron": "",
           "kandidaat_vorige_ronde": row.get("kandidaat_vorige_ronde", "")}
    basis = "https://" + dom
    try:
        r0 = requests.get(basis, headers=H, timeout=18, verify=False, allow_redirects=True)
        if r0.status_code < 400:
            basis = "/".join(r0.url.rstrip("/").split("/")[:3])
    except Exception:
        pass

    gevonden, bronnen = [], []
    for pad in PADEN:
        html = haal(basis, pad)
        time.sleep(0.6)
        if not html:
            continue
        t = tekst(html)
        nav = set()
        for n, f in namen(t, nav):
            if n not in [x for x, _ in gevonden]:
                gevonden.append((n, f))
                if basis + pad not in bronnen:
                    bronnen.append(basis + pad)
        if len(gevonden) >= 3:
            break
    uit["kandidaten"] = "; ".join(f"{n} ({f})" for n, f in gevonden[:4])
    uit["bron"] = bronnen[0] if bronnen else ""
    return uit


def main():
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    print(f"{len(rows)} bedrijven, gratis route", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=5) as ex:
        res = list(ex.map(scan, rows))
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
        w.writeheader(); w.writerows(res)
    raak = sum(1 for r in res if r["kandidaten"])
    print(f"kandidaat gevonden op de eigen site: {raak} van {len(res)}", file=sys.stderr)


if __name__ == "__main__":
    main()
