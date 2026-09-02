#!/usr/bin/env python3
"""Kandidaat-beslissers via Bedrijfsdata, tegen zo min mogelijk credits.

Eén aanroep per bedrijf en dus één credit. Het endpoint /people wil naam EN domein
samen hebben; met alleen een van beide geeft het 403, en dat kost niets. De omweg
via /companies om een company_id op te halen, zoals in Context/tools/bdbeslisser.py,
is daarmee overbodig en scheelt de helft.

Wat eruit komt zijn KANDIDATEN. Bedrijfsdata is een aggregator, en volgens de
beslisser-poort telt een aggregator niet als bewijs. Elke naam hier moet nog
bevestigd worden door een bron waarin het bedrijf de persoon zelf noemt, en een
van de twee bronnen moet jonger zijn dan 90 dagen.

Gebruik:
    python3 beslisser-api.py beslissers-open.csv beslissers-api.csv [aantal]
"""
import csv, json, os, re, ssl, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

BASIS = "https://api.bedrijfsdata.nl/v1.3"
SLEUTELBESTAND = Path.home() / ".pique" / "bedrijfsdata.env"
CTX = ssl.create_default_context()

# De doelrol-ladder. Bij een webshop van deze omvang beslist de eigenaar over
# uitbesteed klantcontact, daarna de operationele of e-commercekant. Iemand op de
# servicedesk zelf voelt de pijn maar tekent niet.
RANG = [
    (re.compile(r"(?i)\b(eigenaar|owner|oprichter|founder|co-?founder|dga)\b"), 5),
    (re.compile(r"(?i)\b(ceo|directeur|director|bestuurder|managing|zaakvoerder)\b"), 5),
    (re.compile(r"(?i)\b(coo|operations?|operationeel)\b"), 4),
    (re.compile(r"(?i)\b(e-?commerce|online|webshop)\b"), 4),
    (re.compile(r"(?i)\b(customer|klantcontact|klantenservice|service manager)\b"), 3),
    (re.compile(r"(?i)\b(cmo|marketing)\b"), 3),
    (re.compile(r"(?i)\b(manager|hoofd|lead)\b"), 2),
]
NIET = re.compile(r"(?i)assistent|medewerk|stagiair|receptie|administrat|monteur|chauffeur|"
                  r"magazijn|logistic|warehouse|intern\b|vacature")


def sleutel():
    k = os.environ.get("BD_API_KEY", "").strip()
    if k:
        return k
    for r in SLEUTELBESTAND.read_text().splitlines():
        if r.strip().startswith("BD_API_KEY"):
            return r.split("=", 1)[1].strip().strip("\"'")
    sys.exit("geen sleutel gevonden")


def score(rol):
    if not rol or NIET.search(rol):
        return 0
    for pat, s in RANG:
        if pat.search(rol):
            return s
    return 1


def bruikbare_voornaam(naam):
    """Een voornaam die je op een kaart kunt schrijven. Initialen en losse letters
    vallen af, want 'Hoi K.' is direct ontmaskerend."""
    n = (naam or "").strip()
    if not n or "," in n:
        return ""
    eerste = n.split()[0].strip(".")
    if len(eerste) < 3 or re.fullmatch(r"(?:[A-Z]\.?){1,4}", eerste) or not eerste[0].isupper():
        return ""
    return eerste


def main():
    key = sleutel()
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    if len(sys.argv) > 3:
        rows = rows[:int(sys.argv[3])]
    uit, credits = [], 0
    for i, r in enumerate(rows, 1):
        naam, dom = r["bedrijf"], (r["domein"] or "").strip()
        rij = {"bedrijf": naam, "domein": dom, "kandidaat": "", "voornaam": "",
               "rol": "", "rang": "", "alternatieven": "", "credits": 0, "notitie": ""}
        if not dom:
            rij["notitie"] = "geen domein"
            uit.append(rij); continue
        q = urllib.parse.urlencode({"name": naam, "domain": dom, "limit": 25, "api_key": key})
        try:
            with urllib.request.urlopen(f"{BASIS}/people?{q}", timeout=35, context=CTX) as f:
                d = json.loads(f.read())
        except urllib.error.HTTPError as e:
            rij["notitie"] = f"http {e.code}"
            uit.append(rij); continue
        except Exception as e:
            rij["notitie"] = str(e)[:60]
            uit.append(rij); continue

        rij["credits"] = d.get("credits_used", 0) or 0
        credits += rij["credits"]
        mensen = d.get("data") or d.get("people") or []
        if not mensen:
            rij["notitie"] = "geen personen"
            uit.append(rij); continue

        kand = []
        for m in mensen:
            vol = (m.get("name") or " ".join(x for x in (m.get("first_name"),
                   m.get("last_name")) if x)).strip()
            rol = (m.get("job_title") or m.get("function") or "").strip()
            s = score(rol)
            vn = bruikbare_voornaam(vol)
            if s and vn:
                kand.append((s, vol, vn, rol))
        if not kand:
            rij["notitie"] = "geen rol uit de ladder"
            rij["alternatieven"] = " | ".join(
                f"{(m.get('name') or '?')}: {m.get('job_title') or '?'}" for m in mensen[:4])[:220]
            uit.append(rij); continue
        kand.sort(key=lambda x: -x[0])
        s, vol, vn, rol = kand[0]
        rij.update(kandidaat=vol, voornaam=vn, rol=rol, rang=str(s),
                   alternatieven=" | ".join(f"{v} ({r})" for _, v, _, r in kand[1:4]))
        uit.append(rij)
        print(f"  {i:>2}/{len(rows)} {naam[:24]:<24} {vol[:26]:<26} {rol[:34]}", flush=True)

    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(uit[0].keys()))
        w.writeheader(); w.writerows(uit)
    raak = sum(1 for r in uit if r["kandidaat"])
    print(f"\n{raak} van {len(uit)} met een kandidaat op een beslissersrol")
    print(f"credits verbruikt: {credits}")


if __name__ == "__main__":
    main()
