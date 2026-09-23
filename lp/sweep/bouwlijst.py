#!/usr/bin/env python3
"""Voegt de drie signaallagen samen tot een gescoorde prospectlijst voor BCS batch 5.

Laag 1  vacature      : wie geeft nu geld uit aan klantcontact (vacaturescrape)
Laag 2  volumebewijs  : webshop, assortiment, markten, ticketsysteem (d2cscan)
Laag 3  serviceopzet  : openingstijden, reactiebelofte, kanalen (bcs-servicescan)

De score weegt bewijs van ticketvolume zwaarder dan bewijs van pijn, want batch 1 tot en
met 3 liepen stuk op bedrijven die te klein waren en niet op bedrijven zonder klacht.
"""
import csv, os, re, glob, sys

HIER = os.path.dirname(os.path.abspath(__file__))
BCS = os.path.dirname(os.path.dirname(HIER))


def norm(n):
    n = (n or "").lower()
    n = re.sub(r"\b(b\.?v\.?|n\.?v\.?|holding|group|groep|nederland|international|inc\.?)\b", " ", n)
    return re.sub(r"[^a-z0-9]", "", n)


def tools_aanwezig(d):
    return [t for t in re.split(r"[|,]", (d.get("cs_tools") or "")) if t and t != "whatsapp"]


def getal(v):
    try:
        return int(float(v or 0))
    except Exception:
        return 0


def lees(pad, sleutel="bedrijf"):
    if not os.path.exists(pad):
        return {}
    return {norm(r[sleutel]): r for r in csv.DictReader(open(pad, encoding="utf-8"))}


# Bedrijven die al een kaart kregen, plus de uitsluitingslijst. Drie manieren, zoals
# afgesproken na de Naif Care-miss in batch 4: naam, domein en de LP-mapnamen.
benaderd = set()
for m in ("bcs", "bcs2", "bcs3", "bcs4"):
    for p in glob.glob(os.path.join(BCS, m, "*.html")):
        benaderd.add(re.sub(r"[^a-z0-9]", "", os.path.basename(p)[:-5].lower()))
uitgesloten, uitdomein = set(), set()
for r in csv.DictReader(open(os.path.join(BCS, "BCS-Batch4-FaseA-Uitgesloten.csv"), encoding="utf-8")):
    uitgesloten.add(norm(r["bedrijf"]))
    if r.get("domein"):
        uitdomein.add(r["domein"].lower().replace("www.", ""))
pooldomein = set()
for r in csv.DictReader(open(os.path.join(HIER, "pool-alles.csv"), encoding="utf-8")):
    if r.get("al_benaderd") == "ja" and r.get("domein"):
        pooldomein.add(r["domein"].lower().replace("www.", ""))

d2c = lees(os.path.join(HIER, "d2c-scan-alles.csv"))
rev = lees(os.path.join(HIER, "reviewscan.csv"))
srv = lees(os.path.join(HIER, "servicescan-nieuw.csv"))

uit = []
for sleutel, d in d2c.items():
    if d.get("webshop") != "ja":
        continue
    dom = (d.get("domein") or "").lower().replace("www.", "")
    if sleutel in benaderd or sleutel in uitgesloten or dom in uitdomein or dom in pooldomein:
        continue
    r, s = rev.get(sleutel, {}), srv.get(sleutel, {})
    prod, markt = getal(d.get("producten")), getal(d.get("markten"))
    score, waarom = 0, []

    # Criterium 02 uit het ICP: Shopify heeft voorrang, andere echte webshopplatforms
    # tellen mee. Beslist door Simon op 22 september 2026, omdat het platform bepaalt
    # hoe makkelijk BCS kan koppelen en niet of het bedrijf een probleem heeft.
    if "shopify" in (d.get("platform") or ""):
        score += 2; waarom.append("Shopify")
    elif d.get("platform"):
        score += 1; waarom.append(d["platform"].split("|")[0])

    # Bandtoets 3 tot 20 miljoen. Omzet is niet machinaal te halen, dus we schatten op
    # volumebewijs. Te weinig bewijs is onderkant, te veel is een concern met een eigen
    # afdeling. Allebei buiten de band.
    tekenen = sum([bool(tools_aanwezig(d)), markt >= 6, prod >= 300, bool(d.get("review_tools"))])
    if tekenen == 0:
        score -= 3; waarom.append("te weinig volumebewijs voor de band")
    if markt >= 30 and prod >= 1000:
        score -= 2; waarom.append("mogelijk boven de band")

    # Laag 2, bewijs van ticketvolume. Dit weegt het zwaarst.
    tools = [t for t in re.split(r"[|,]", (d.get("cs_tools") or "")) if t and t != "whatsapp"]
    if tools:
        score += 3; waarom.append("betaalt voor " + "/".join(tools))
    if markt >= 12:
        score += 3; waarom.append(f"{markt} markten")
    elif markt >= 6:
        score += 2; waarom.append(f"{markt} markten")
    if prod >= 1000:
        score += 3; waarom.append(f"{prod}+ artikelen")
    elif prod >= 300:
        score += 2; waarom.append(f"{prod} artikelen")
    elif prod >= 100:
        score += 1; waarom.append(f"{prod} artikelen")
    if d.get("review_tools"):
        score += 2; waarom.append("eigen reviewplatform")
    if d.get("b2b"):
        score += 1; waarom.append("b2b naast d2c")

    # Laag 3, de serviceopzet. Dit levert de bevinding voor de pagina.
    tijden = (s.get("openingstijden") or "").strip()
    if tijden:
        uren = [int(h) for h, _ in re.findall(r"(\d{1,2})[:.](\d{2})", tijden)]
        if uren and max(uren) <= 17:
            score += 2; waarom.append("desk dicht voor de avond")
        if "donderdag" in tijden.lower() and "vrijdag" not in tijden.lower():
            score += 2; waarom.append("vierdaagse week")
    if (s.get("reactiebelofte") or "").strip():
        score += 2; waarom.append("belofte: " + s["reactiebelofte"].strip())
    if not (s.get("telefoon") or "").strip():
        score += 1; waarom.append("geen telefoonlijn gevonden")

    # Laag 1, de vacature. Alleen een echte klantcontactvacature telt als trigger, en
    # vers telt dubbel. Een vacature voor een fotobewerker zegt niets over klantcontact.
    if d.get("is_cs") == "ja":
        score += 3
        waarom.append("zoekt klantcontact: " + (d.get("functie") or "")[:40])
        if (d.get("datum") or "") >= "2026-06-24":
            score += 2; waarom.append("vacature staat nog open")
    else:
        score -= 2

    if (r.get("reviewoordeel") or "") == "zwak":
        score += 3; waarom.append("publiceert zelf een zwakke score")

    uit.append({
        "score": score, "bedrijf": d["bedrijf"], "domein": d["domein"],
        "vacature": d.get("functie", ""), "vacature_datum": d.get("datum", ""),
        "plaats": d.get("plaats", ""), "producten": d.get("producten", ""),
        "markten": d.get("markten", ""), "cs_tools": d.get("cs_tools", ""),
        "review_tools": d.get("review_tools", ""),
        "reviewscore": r.get("reviewscore", ""), "reviewoordeel": r.get("reviewoordeel", ""),
        "openingstijden": s.get("openingstijden", ""), "reactiebelofte": s.get("reactiebelofte", ""),
        "email": s.get("email", ""), "telefoon": s.get("telefoon", ""),
        "kvk": d.get("kvk", ""), "postcode": d.get("postcode", ""),
        "signalen": "; ".join(waarom), "vacature_url": d.get("vacature_url", ""),
    })

uit.sort(key=lambda x: -x["score"])
doel = os.path.join(HIER, "batch5-kandidaten.csv")
with open(doel, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(uit[0].keys()))
    w.writeheader(); w.writerows(uit)
print(f"{len(uit)} kandidaten -> {doel}")
for grens in (10, 8, 6, 4):
    print(f"  score {grens}+ : {sum(1 for x in uit if x['score'] >= grens)}")
