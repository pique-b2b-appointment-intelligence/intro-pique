#!/usr/bin/env python3
"""Eén pass over de site van elke prospect, drie controles tegelijk.

1. Adres: staat de postcode of de straat uit Bedrijfsdata ook op hun eigen site?
   Het BAG-id zegt alleen dat het adres bestaat, niet dat dit bedrijf er zit.
2. Naam: staat de achternaam van de kandidaat op hun eigen site?
3. Oogst: noemt de site zelf een voornaam die we nog niet hadden?

Alles wat hier bevestigd wordt, is het bedrijf dat zichzelf noemt. Dat is de tweede
bron die de beslisser-poort vraagt.
"""
import csv, re, sys, time, unicodedata, warnings
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings("ignore")
import requests
requests.packages.urllib3.disable_warnings()

H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
     "Accept-Language": "nl-NL,nl;q=0.9"}
# De homepage staat er bewust als eerste in: bij veel webshops staat het adres alleen
# in de voettekst, en die stond in de vorige versie niet in de lijst.
PADEN = ["", "/pages/contact", "/contact", "/pages/over-ons", "/over-ons", "/about",
         "/about-us", "/pages/algemene-voorwaarden", "/algemene-voorwaarden",
         "/pages/about", "/policies/terms-of-service", "/klantenservice", "/team",
         "/pages/team", "/pages/bedrijfsgegevens", "/nl/contact", "/service/about",
         "/pages/veelgestelde-vragen", "/privacy", "/pages/privacy-policy"]
# Iemand die zich voorstelt of ondertekent. Streng, want een verzonnen naam kost de kaart.
VOORNAAM = [
    r"\bik ben ([A-Z][a-zé]{2,12})\b",
    r"\bmijn naam is ([A-Z][a-zé]{2,12})\b",
    r"(?:groetjes|groet|liefs),?\s*([A-Z][a-zé]{2,12})\b",
    r"\bopgericht door ([A-Z][a-zé]{2,12})\b",
    r"\bdoor ([A-Z][a-zé]{2,12}) opgericht\b",
    r"\boprichter[,:]?\s+([A-Z][a-zé]{2,12})\b",
]
GEEN = {"Onze", "Deze", "Alle", "Nederland", "Belgie", "Shopify", "Klarna", "Cookie", "Het",
        "Privacy", "Algemene", "Contact", "Service", "Team", "Home", "Over", "Nieuw", "Ins",
        "Gratis", "Retour", "Klant", "Voor", "Lees", "Bekijk", "Meer", "Ontdek", "Kwaliteit",
        "Wij", "Onze", "Een", "Van", "Met", "Sinds", "Werken", "Vanaf"}


def plat(s):
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s))


def tekst(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))


def scan(row):
    o = dict(row, adres_bevestigd="", naam_bevestigd="", geoogste_voornaam="", bron="", postcodes_op_site="")
    dom = (row.get("domein") or "").strip()
    if not dom:
        return o
    basis = "https://" + dom
    try:
        r0 = requests.get(basis, headers=H, timeout=15, verify=False, allow_redirects=True)
        if r0.status_code < 400:
            basis = "/".join(r0.url.rstrip("/").split("/")[:3])
    except Exception:
        pass

    body = ""
    for pad in PADEN:
        try:
            r = requests.get(basis + pad, headers=H, timeout=15, verify=False)
        except Exception:
            continue
        time.sleep(0.4)
        if r.status_code == 200 and len(r.text) > 800:
            # Grote Shopify-homepages lopen tot ver boven een megabyte. Zonder deze
            # begrenzing loopt het geheugen vol en wordt het proces afgeschoten.
            body += " " + tekst(r.text[:400000])
            if len(body) > 150000:
                break
    if not body:
        return o
    p = plat(body)

    o["postcodes_op_site"] = " ".join(sorted(set(
        re.sub(r"\s+", "", x).upper() for x in re.findall(r"\b\d{4}\s?[A-Z]{2}\b", body))))[:120]
    pc = re.sub(r"\s+", "", row.get("postcode", "")).lower()
    straat = plat(re.sub(r"\d+.*$", "", row.get("adres", ""))).strip()
    if pc and pc in re.sub(r"\s+", "", p):
        o["adres_bevestigd"] = "postcode op de eigen site"
    elif straat and len(straat) > 5 and straat in p:
        o["adres_bevestigd"] = "straatnaam op de eigen site"

    naam = (row.get("naam") or "").strip()
    if naam and len(naam.split()) > 1:
        achter = plat(naam.split()[-1])
        if len(achter) > 3 and re.search(r"\b" + re.escape(achter) + r"\b", p):
            o["naam_bevestigd"] = "achternaam op de eigen site"

    if not naam:
        for pat in VOORNAAM:
            m = re.search(pat, body)
            if m and m.group(1) not in GEEN:
                o["geoogste_voornaam"] = m.group(1)
                o["bron"] = re.sub(r"\s+", " ", body[max(0, m.start()-70):m.end()+70]).strip()[:150]
                break
    return o


def main():
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    print(f"{len(rows)} bedrijven, een pass per site", file=sys.stderr)
    res = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        for i, r in enumerate(ex.map(scan, rows), 1):
            res.append(r)
            if i % 10 == 0:
                print(f"  {i}/{len(rows)}", file=sys.stderr, flush=True)
                with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
                    w.writeheader(); w.writerows(res)
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
        w.writeheader(); w.writerows(res)
    print(f"adres bevestigd op eigen site : {sum(1 for r in res if r['adres_bevestigd'])}")
    print(f"naam bevestigd op eigen site  : {sum(1 for r in res if r['naam_bevestigd'])}")
    print(f"nieuwe voornaam geoogst       : {sum(1 for r in res if r['geoogste_voornaam'])}")


if __name__ == "__main__":
    main()
