#!/usr/bin/env python3
"""Toetst een kandidaat-beslisser tegen de site van het bedrijf zelf.

De beslisser-poort vraagt twee onafhankelijke bronnen, en een aggregator telt niet
als bewijs. Deze toets levert de tweede bron op de goedkoopste manier die er is:
staat de naam op hun eigen site, dan noemt het bedrijf de persoon zelf.

Een treffer op alleen de voornaam telt niet, want die kan van iedereen zijn. Het
gaat om de achternaam, of om voornaam en achternaam dicht bij elkaar.

Gebruik:
    python3 beslisser-toets.py beslissers-api.csv beslissers-getoetst.csv
"""
import csv, re, sys, time, unicodedata, warnings
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings("ignore")
import requests
requests.packages.urllib3.disable_warnings()

H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
     "Accept-Language": "nl-NL,nl;q=0.9"}
PADEN = ["", "/pages/over-ons", "/over-ons", "/pages/about", "/about", "/about-us",
         "/pages/ons-verhaal", "/team", "/pages/team", "/contact", "/pages/contact"]


def plat(s):
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s))


def toets(row):
    uit = dict(row, bevestigd="", bevestigingsbron="")
    kand = row.get("kandidaat", "").strip()
    dom = row.get("domein", "").strip()
    if not kand or not dom:
        return uit
    delen = kand.split()
    achter = plat(delen[-1])
    voor = plat(delen[0])
    if len(achter) < 3:
        uit["bevestigd"] = "achternaam te kort om op te toetsen"
        return uit

    basis = "https://" + dom
    try:
        r0 = requests.get(basis, headers=H, timeout=18, verify=False, allow_redirects=True)
        if r0.status_code < 400:
            basis = "/".join(r0.url.rstrip("/").split("/")[:3])
    except Exception:
        pass

    for pad in PADEN:
        try:
            r = requests.get(basis + pad, headers=H, timeout=18, verify=False)
        except Exception:
            continue
        time.sleep(0.5)
        if r.status_code != 200 or len(r.text) < 800:
            continue
        t = plat(re.sub(r"<[^>]+>", " ", r.text))
        if re.search(r"\b" + re.escape(achter) + r"\b", t):
            uit["bevestigd"] = "achternaam op de eigen site"
            uit["bevestigingsbron"] = basis + pad
            return uit
        if voor and re.search(r"\b" + re.escape(voor) + r"\b", t):
            uit["bevestigd"] = "alleen voornaam op de site, te zwak"
            uit["bevestigingsbron"] = basis + pad
    return uit


def main():
    rows = [r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8")) if r["kandidaat"]]
    # namen die bij meer dan een bedrijf voorkomen zijn een datafout, die slaan we over
    import collections
    tel = collections.Counter(r["kandidaat"] for r in rows)
    rows = [r for r in rows if tel[r["kandidaat"]] == 1]
    print(f"{len(rows)} unieke kandidaten toetsen", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=5) as ex:
        res = list(ex.map(toets, rows))
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
        w.writeheader(); w.writerows(res)
    hard = sum(1 for r in res if r["bevestigd"] == "achternaam op de eigen site")
    zwak = sum(1 for r in res if r["bevestigd"].startswith("alleen voornaam"))
    print(f"bevestigd door het bedrijf zelf: {hard}", file=sys.stderr)
    print(f"alleen voornaam gevonden, te zwak: {zwak}", file=sys.stderr)
    print(f"niet gevonden op de eigen site: {len(res)-hard-zwak}", file=sys.stderr)


if __name__ == "__main__":
    main()
