#!/usr/bin/env python3
"""Haalt het adres op zoals het bedrijf het zelf op zijn site zet.

Waarom dit boven het handelsregister gaat: het register geeft de statutaire vestiging,
en dat kan het kantoor van de accountant of een holdingadres zijn. Het adres op hun
eigen contactpagina is waar de post ook echt aankomt.

Zoekt een postcodepatroon en leest de straat met huisnummer die er vlak voor staat.
Alleen als beide er staan telt het.
"""
import csv, re, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings("ignore")
import requests
requests.packages.urllib3.disable_warnings()

H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
     "Accept-Language": "nl-NL,nl;q=0.9"}
PADEN = ["/pages/contact", "/contact", "", "/pages/algemene-voorwaarden",
         "/algemene-voorwaarden", "/policies/terms-of-service", "/klantenservice",
         "/pages/over-ons", "/over-ons", "/pages/bedrijfsgegevens"]
# straat met huisnummer, dan postcode, dan plaats
ADRES = re.compile(
    r"([A-Z][A-Za-zäëïöüéèáà'\.\- ]{3,34}?\s+\d{1,4}\s?[A-Za-z]{0,3})"
    r"[,\s]+(\d{4}\s?[A-Z]{2})[,\s]+([A-Z][A-Za-zäëïöü'\-\s]{2,24})")


def tekst(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("<br>", ", "), ("<br/>", ", "), ("<br />", ", ")):
        h = h.replace(a, b)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", ", ", h))


def scan(row):
    o = dict(row, site_adres="", site_postcode="", site_plaats="", site_bron="")
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
    for pad in PADEN:
        try:
            r = requests.get(basis + pad, headers=H, timeout=18, verify=False)
        except Exception:
            continue
        time.sleep(0.5)
        if r.status_code != 200 or len(r.text) < 800:
            continue
        m = ADRES.search(tekst(r.text[:400000]))
        if m:
            straat = re.sub(r"[,\s]+$", "", m.group(1)).strip(" ,")
            plaats = re.sub(r"\s+", " ", m.group(3)).strip(" ,")
            if len(straat) > 4 and len(plaats) > 2:
                o.update(site_adres=straat, site_postcode=re.sub(r"\s+", "", m.group(2)).upper(),
                         site_plaats=plaats, site_bron=basis + pad)
                return o
    return o


def main():
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    print(f"{len(rows)} bedrijven", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=3) as ex:
        res = list(ex.map(scan, rows))
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
        w.writeheader(); w.writerows(res)
    raak = [r for r in res if r["site_postcode"]]
    print(f"adres op de eigen site gevonden: {len(raak)} van {len(res)}\n")
    for r in raak:
        gelijk = "zelfde" if re.sub(r"\s+", "", r.get("postcode", "")).upper() == r["site_postcode"] else "ANDER"
        print(f"  {r['bedrijf'][:22]:<22} {r['site_adres'][:28]:<28} {r['site_postcode']:<8} "
              f"{r['site_plaats'][:16]:<16} {gelijk}")


if __name__ == "__main__":
    main()
