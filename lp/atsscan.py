#!/usr/bin/env python3
"""Zoekt openstaande klantcontact-vacatures via het sollicitatiesysteem van de prospect.

Waarom dit de sterkste machineroute is voor BCS: een openstaande vacature voor
klantenservice is het enige signaal dat zowel door triggercheck.py komt als precies
over de propositie gaat. Bij Matt Sleeps leverde het drie goedgekeurde triggers op,
terwijl van negen handmatig gezochte triggers er maar een doorkwam.

De vorige poging gokte de bedrijfsnaam op drie ATS-hosts en vond er twee. Dit script
doet het andersom en dat is de hele winst:

  1. haal de werken-bij-link van hun eigen site
  2. kijk welk systeem daarachter zit
  3. lees de publieke API van dat systeem
  4. lukt dat niet, lees dan de vacaturetitels van de pagina zelf

Alleen vacatures met een datum tellen mee, want zonder datum is het geen trigger.

Gebruik:
    python3 atsscan.py <in.csv met bedrijf en domein> <uit.csv>
"""
import csv, json, re, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
warnings.filterwarnings("ignore")
import requests
requests.packages.urllib3.disable_warnings()

H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
     "Accept-Language": "nl-NL,nl;q=0.9"}
WERKENBIJ = re.compile(r"(werken-?bij|vacature|career|jobs|join-?us|meewerken|team/vacatures)", re.I)
KLANT = re.compile(r"(customer|klant|service|support|care|helpdesk|webcare)", re.I)

# Publieke eindpunten per sollicitatiesysteem. De sleutel is wat je in de HTML ziet staan.
ATS = {
    "recruitee.com":   lambda s: (f"https://{s}.recruitee.com/api/offers/", "offers"),
    "homerun.co":      lambda s: (f"https://api.homerun.co/v1/{s}/jobs", None),
    "personio":        lambda s: (f"https://{s}.jobs.personio.de/search.json", None),
    "teamtailor.com":  lambda s: (f"https://{s}.teamtailor.com/jobs.json", "jobs"),
    "greenhouse.io":   lambda s: (f"https://boards-api.greenhouse.io/v1/boards/{s}/jobs", "jobs"),
    "workable.com":    lambda s: (f"https://apply.workable.com/api/v1/widget/accounts/{s}?details=true", "jobs"),
}


def haal(url, timeout=18):
    try:
        r = requests.get(url, headers=H, timeout=timeout, verify=False, allow_redirects=True)
        return r if r.status_code == 200 else None
    except Exception:
        return None


# Een pagina is pas een vacaturepagina als er ook echt over solliciteren wordt gepraat.
# Zonder deze toets pikt de scanner navigatielinks op als "Klantenservice" en "Careers".
IS_VACATUREPAGINA = re.compile(
    r"(solliciteer|sollicitatie|wat ga je doen|wie ben jij|uur per week|"
    r"fulltime|parttime|arbeidsvoorwaarden|salaris|vacature)", re.I)
# Een vacaturetitel bevat een rol, geen paginanaam. "Klantenservice" alleen is geen vacature.
ROL = re.compile(r"(medewerk\w*|agent|specialist|adviseur|manager|adviseur|"
                 r"consultant|representative|assistent|coordinator|lead)\b", re.I)
NIETVACATURE = re.compile(r"(terms|voorwaarden|guide|policy|privacy|cookie|contact|"
                          r"veelgestelde|faq|retour|verzend)", re.I)


def titels_uit_pagina(html):
    """Laatste redmiddel als er geen sollicitatiesysteem achter zit.

    Streng afgesteld met opzet: een gemiste vacature kost niets, een verzonnen vacature
    zet een onwaarheid op de landingspagina.
    """
    uit = []
    for m in re.finditer(r"<(h[1-4]|a)[^>]*>(.{6,80}?)</\1>", html, re.S | re.I):
        t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(2))).strip()
        if len(t.split()) < 2 or NIETVACATURE.search(t):
            continue
        # Op een overzichtspagina staat elke vacature als link. Een functietitel bevat
        # een rolwoord; een menu-item als "Klantenservice" doet dat niet.
        if KLANT.search(t) and ROL.search(t) and t not in uit:
            uit.append(t)
    return uit[:4]


def scan(row):
    o = {"bedrijf": row["bedrijf"], "domein": row["domein"], "ats": "", "vacature_url": "",
         "cs_vacatures": "", "alle_vacatures": 0, "bron": ""}
    dom = (row.get("domein") or "").strip()
    if not dom:
        return o
    basis = "https://" + dom
    r0 = haal(basis)
    if r0 is None:
        return o
    basis = "/".join(r0.url.rstrip("/").split("/")[:3])
    html = r0.text[:400000]

    # 1. de werken-bij-link zoeken, op de homepage en op een paar vaste paden
    kandidaten = []
    for m in re.finditer(r'href="([^"]{3,160})"', html):
        u = m.group(1)
        if WERKENBIJ.search(u):
            kandidaten.append(urljoin(basis + "/", u))
    for pad in ("/pages/vacatures", "/vacatures", "/werken-bij", "/careers", "/jobs",
                "/pages/werken-bij", "/over-ons/vacatures"):
        kandidaten.append(basis + pad)
    kandidaten = list(dict.fromkeys(kandidaten))[:8]

    # 2. welk systeem zit erachter
    for u in kandidaten:
        r = haal(u)
        time.sleep(0.4)
        if r is None or len(r.text) < 500:
            continue
        o["vacature_url"] = r.url
        h = r.text[:400000]
        stam = re.sub(r"[^a-z0-9]", "", urlparse(basis).netloc.split(".")[-2])
        for merk, bouw in ATS.items():
            kern = re.escape(merk.split(".")[0])
            m = re.search(r"https?://([a-z0-9\-]{2,40})\." + kern + r"\.", h, re.I)
            if merk == "personio":
                m = re.search(r"https?://([a-z0-9\-]{2,40})\.jobs\.personio\.[a-z]+", h, re.I)
            if merk == "greenhouse.io":
                m = re.search(r"greenhouse\.io/(?:embed/job_board\?for=)?([a-z0-9\-]{2,40})", h, re.I)
            if merk == "workable.com":
                m = re.search(r"apply\.workable\.com/([a-z0-9\-]{2,40})", h, re.I)
            slug = m.group(1) if m else None
            if slug in ("www", "jobs", "careers", "career", "api", "app"):
                slug = stam          # een generieke subdomeinnaam is niet de slug
            if not slug and kern in h.lower():
                slug = stam          # merk genoemd maar geen slug, probeer de domeinstam
            if slug:
                api, sleutel = bouw(slug)
                # 3. de publieke API lezen
                ra = haal(api, timeout=25)
                if ra is not None:
                    try:
                        d = ra.json()
                    except Exception:
                        d = None
                    rijen = (d.get(sleutel) if isinstance(d, dict) and sleutel else
                             d if isinstance(d, list) else
                             (d.get("jobs") or d.get("offers") or d.get("data") or []) if isinstance(d, dict) else [])
                    if isinstance(rijen, list) and rijen:
                        o["ats"] = f"{merk} ({slug})"
                        o["alle_vacatures"] = len(rijen)
                        cs = []
                        for v in rijen:
                            titel = str(v.get("title") or v.get("name") or "")
                            afd = str(v.get("department") or v.get("departmentName") or "")
                            if KLANT.search(titel) or KLANT.search(afd):
                                datum = str(v.get("created_at") or v.get("published_at") or
                                            v.get("first_published") or v.get("updated_at") or "")[:10]
                                cs.append(f"{titel} | {datum}")
                        o["cs_vacatures"] = " ;; ".join(cs)
                        o["bron"] = api
                        return o
                break
        # 3b. geen systeem in de HTML gevonden: probeer de domeinstam als slug. Veel
        # bedrijven linken naar een eigen werkenbij-domein waar de ATS-naam niet in staat,
        # terwijl <domeinstam>.recruitee.com wel gewoon bestaat.
        if not o["ats"]:
            for merk in ("recruitee.com", "homerun.co", "teamtailor.com"):
                api, sleutel = ATS[merk](stam)
                ra = haal(api, timeout=20)
                if ra is None:
                    continue
                try:
                    d = ra.json()
                except Exception:
                    continue
                rijen = d.get(sleutel) if isinstance(d, dict) and sleutel else (d if isinstance(d, list) else [])
                if isinstance(rijen, list) and rijen:
                    o["ats"] = f"{merk} ({stam})"
                    o["alle_vacatures"] = len(rijen)
                    cs = []
                    for v in rijen:
                        titel = str(v.get("title") or v.get("name") or "")
                        afd = str(v.get("department") or "")
                        if KLANT.search(titel) or KLANT.search(afd):
                            datum = str(v.get("created_at") or v.get("published_at") or "")[:10]
                            cs.append(f"{titel} | {datum}")
                    o["cs_vacatures"] = " ;; ".join(cs)
                    o["bron"] = api
                    return o

        # 4. geen systeem herkend, dan de vacaturelinks van de pagina zelf lezen
        t = titels_uit_pagina(h)
        if t:
            o["cs_vacatures"] = " ;; ".join(f"{x} | zonder datum" for x in t)
            o["bron"] = r.url
            return o
    return o


def main():
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    print(f"{len(rows)} bedrijven", file=sys.stderr)
    res = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for i, r in enumerate(ex.map(scan, rows), 1):
            res.append(r)
            if r["cs_vacatures"]:
                print(f"  {r['bedrijf'][:22]:<22} {r['ats'][:22]:<22} {r['cs_vacatures'][:70]}", flush=True)
            if i % 20 == 0:
                with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
                    w.writeheader(); w.writerows(res)
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
        w.writeheader(); w.writerows(res)
    print(f"\nsollicitatiesysteem herkend : {sum(1 for r in res if r['ats'])}")
    print(f"klantcontact-vacature open  : {sum(1 for r in res if r['cs_vacatures'])}")


if __name__ == "__main__":
    main()
