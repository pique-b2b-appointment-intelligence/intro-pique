#!/usr/bin/env python3
"""Zoekt een voornaam op de site van het bedrijf zelf.

Voor de aanhef op een handgeschreven kaart is een voornaam genoeg. Veel kleine
webshops noemen nergens een volledige naam, maar tekenen hun over-ons-pagina wel
met "Groetjes, Sanne" of schrijven "ik ben Dominique". Dat is de goedkoopste
bruikbare bron die er is, en het is het bedrijf dat zichzelf noemt.

Alleen patronen waarin iemand zichzelf voorstelt of ondertekent tellen mee. Een
losse hoofdletterwoord ergens op de pagina is geen naam.
"""
import csv, re, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings("ignore")
import requests
requests.packages.urllib3.disable_warnings()

H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
     "Accept-Language": "nl-NL,nl;q=0.9"}
PADEN = ["/pages/over-ons", "/over-ons", "/pages/about", "/about", "/about-us", "/over",
         "/pages/ons-verhaal", "/ons-verhaal", "/team", "/pages/team", "/service/about",
         "/pages/contact", "/contact", "/nl/over-yogisha"]
# Iemand die zich voorstelt of ondertekent.
PATRONEN = [
    r"\bik ben ([A-Z][a-zé]{2,12})\b",
    r"\bmijn naam is ([A-Z][a-zé]{2,12})\b",
    r"\b(?:groetjes|groet|liefs|xxx?),?\s*([A-Z][a-zé]{2,12})\b",
    r"\boprichter,?\s*([A-Z][a-zé]{2,12})\b",
    r"\b([A-Z][a-zé]{2,12})\s*(?:&|en)\s*([A-Z][a-zé]{2,12})\b(?=[^.]{0,40}(?:oprich|eigena|samen|runnen))",
    r"\bdoor ([A-Z][a-zé]{2,12}) opgericht\b",
    r"\bopgericht door ([A-Z][a-zé]{2,12})\b",
]
GEEN = {"Onze", "Deze", "Alle", "Nederland", "Belgie", "Shopify", "Klarna", "Cookie",
        "Privacy", "Algemene", "Contact", "Service", "Team", "Home", "Over", "Nieuw",
        "Gratis", "Retour", "Klant", "Voor", "Lees", "Bekijk", "Meer", "Ontdek"}


def tekst(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))


def scan(row):
    o = {"bedrijf": row["bedrijf"], "domein": row["domein"], "voornaam": "", "zin": "", "bron": ""}
    dom = row["domein"].strip()
    if not dom:
        return o
    basis = "https://" + dom
    try:
        r0 = requests.get(basis, headers=H, timeout=15, verify=False, allow_redirects=True)
        if r0.status_code < 400:
            basis = "/".join(r0.url.rstrip("/").split("/")[:3])
    except Exception:
        pass
    for pad in PADEN:
        try:
            r = requests.get(basis + pad, headers=H, timeout=15, verify=False)
        except Exception:
            continue
        time.sleep(0.4)
        if r.status_code != 200 or len(r.text) < 800:
            continue
        t = tekst(r.text)
        for pat in PATRONEN:
            m = re.search(pat, t)
            if m:
                naam = m.group(1)
                if naam in GEEN:
                    continue
                o.update(voornaam=naam, zin=re.sub(r"\s+", " ", t[max(0, m.start()-60):m.end()+60]).strip(),
                         bron=basis + pad)
                return o
    return o


def main():
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    with ThreadPoolExecutor(max_workers=5) as ex:
        res = list(ex.map(scan, rows))
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
        w.writeheader(); w.writerows(res)
    raak = [r for r in res if r["voornaam"]]
    print(f"voornaam gevonden op de eigen site: {len(raak)} van {len(res)}\n")
    for r in raak:
        print(f"  {r['bedrijf'][:22]:<22} {r['voornaam']:<12} \"{r['zin'][:70]}\"")


if __name__ == "__main__":
    main()
