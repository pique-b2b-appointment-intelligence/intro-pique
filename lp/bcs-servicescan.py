#!/usr/bin/env python3
"""Haalt de letterlijke servicebeloftes van de prospect zelf op.

Waarom letterlijk: de LP-standaard vraagt als bewijs een citaat met domein en
datum, geen bronregel. Een bronregel is een bewering. Een zin die er letterlijk
staat, kan de prospect in dertig seconden zelf controleren.

Alles wat hier uitkomt is dus overgetypt van hun eigen pagina, met de datum
waarop ik het zag. Wat ik niet letterlijk vond, blijft leeg en gaat de pagina
niet op.

Gebruik:
    python3 bcs-servicescan.py ../BCS-Batch4-Researchpool.csv bcs-servicescan.csv
"""
import csv, re, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings("ignore")
import requests
requests.packages.urllib3.disable_warnings()

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
H = {"User-Agent": UA, "Accept-Language": "nl-NL,nl;q=0.9"}
PATHS = ["/pages/contact", "/contact", "/klantenservice", "/pages/klantenservice",
         "/pages/veelgestelde-vragen", "/pages/faq", "/faq", "/service", "/contact-us",
         "/pages/retourneren", "/retourneren", "/pages/customer-service",
         "/nl/contact", "/pages/help", "/klantenservice/contact"]


def tekst(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&#8211;", "-"), ("&ndash;", "-"),
                 ("&#39;", "'"), ("&quot;", '"')):
        h = h.replace(a, b)
    return re.sub(r"\s+", " ", h)


def net(s):
    """Ruimt witruimte op en verder niets.

    Bewust geen hoofdletter aan het begin: deze zin komt in een citaatblok en
    hoort dus letterlijk te staan zoals hij op hun pagina staat. Een hoofdletter
    toevoegen is al een bewerking, en dan is het geen citaat meer.
    """
    return re.sub(r"\s+", " ", (s or "")).strip(" :;,-")


def scan(row):
    dom = (row.get("website") or row.get("domein") or "").strip()
    o = {"bedrijf": row["bedrijf"], "domein": dom, "openingstijden": "",
         "reactiebelofte": "", "email": "", "telefoon": "", "whatsapp": "",
         "chat": "", "retourtermijn": "", "gecheckt": "17 augustus 2026"}
    # eerst het echte basisadres bepalen, want veel shops sturen door naar www of
    # naar een taalpad. Zonder die stap krijg je op elk pad een 404.
    basis = "https://" + dom
    try:
        r0 = requests.get(basis, headers=H, timeout=15, verify=False, allow_redirects=True)
        if r0.status_code < 400:
            basis = "/".join(r0.url.rstrip("/").split("/")[:3])
    except Exception:
        pass

    body = ""
    for p in PATHS:
        r = None
        # Shopify knijpt af met 429 zodra je te snel achter elkaar vraagt. Rustig
        # aan doen en een keer opnieuw proberen is goedkoper dan een lege scan.
        for poging in range(3):
            try:
                r = requests.get(basis + p, headers=H, timeout=20, verify=False)
            except Exception:
                r = None
            if r is not None and r.status_code != 429:
                break
            time.sleep(4 + 4 * poging)
        time.sleep(0.8)
        if r is not None and r.status_code == 200 and len(r.text) > 1200:
            body += " " + tekst(r.text)
            if len(body) > 400000:
                break
    if not body:
        return o

    m = re.search(r"((?:maandag|ma)\b[^.!?]{0,90}?\d{1,2}[:.]\d{2}[^.!?]{0,40}?\d{1,2}[:.]\d{2})",
                  body, re.I)
    if m:
        o["openingstijden"] = net(m.group(1))
    # alleen een reactiebelofte in uren of enkele werkdagen. "binnen 14 dagen" is
    # bijna altijd de retourtermijn en zou de prospect terecht betwisten.
    for pat in (r"binnen\s+\d{1,2}\s*(?:uur|uren)", r"within\s+\d{1,2}\s*hours?",
                r"binnen\s+[1-5]\s*werkdag\w*", r"within\s+[1-5]\s*business days?"):
        m = re.search(pat, body, re.I)
        if m:
            o["reactiebelofte"] = net(m.group(0))
            break
    m = re.search(r"[\w.\-]+@[\w\-]+\.[a-z]{2,8}", body)
    if m:
        o["email"] = m.group(0).lower()
    m = re.search(r"(\+31|\+32|0)[\s\-]?\d{1,3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}", body)
    if m:
        o["telefoon"] = re.sub(r"\s+", " ", m.group(0)).strip()
    if re.search(r"wa\.me/|api\.whatsapp\.com|whatsapp", body, re.I):
        o["whatsapp"] = "ja"
    if re.search(r"\bchat\b", body, re.I):
        o["chat"] = "ja"
    m = re.search(r"\b(\d{1,3})\s*dagen\b[^.!?]{0,24}(retour|bedenktijd|ruilen)", body, re.I)
    if m:
        o["retourtermijn"] = m.group(1) + " dagen"
    return o


def main():
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    print(f"{len(rows)} prospects", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=4) as ex:
        res = list(ex.map(scan, rows))
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
        w.writeheader(); w.writerows(res)
    print("openingstijden:", sum(1 for r in res if r["openingstijden"]),
          "| reactiebelofte:", sum(1 for r in res if r["reactiebelofte"]),
          "| e-mailadres:", sum(1 for r in res if r["email"]),
          "| telefoon:", sum(1 for r in res if r["telefoon"]), file=sys.stderr)


if __name__ == "__main__":
    main()
