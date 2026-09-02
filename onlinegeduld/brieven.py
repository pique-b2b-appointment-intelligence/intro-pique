#!/usr/bin/env python3
"""Bouwt de mail-merge CSV voor de vijftig handgeschreven kaarten van Online Geduld.

Canonieke 17 kolommen, zie Agents/brieven-csv-agent.md. De brieftekst wordt hier
geschreven: onder de vijftig woorden, observatie eerst, het webadres kaal in de
slotzin, en alleen de voornaam van de afzender eronder.
"""
import csv, re, hashlib, collections, sys, os

MAP = "/Users/simonkempers/Desktop/Pique - B2B Appointment Intelligence/Klanten/Online-Geduld"
BASIS = "intro-pique.agency/onlinegeduld"
AFZENDER = "Cheraldo"

def kies(lijst, sleutel, zout=''):
    return lijst[int(hashlib.sha1((sleutel + '|' + zout).encode()).hexdigest(), 16) % len(lijst)]

# ── de observatie, per denkpad, in zijn eigen woorden ────────────────
OPENING = {
 'gids': [
  "Ik zocht {termen} in {plaats} en kwam je tegen in de bedrijvengids. Adres, telefoonnummer, meer niet. Je eigen site heb ik niet kunnen vinden.",
  "Ik ben deze maand {termen} in de regio langsgegaan. Van jullie vond ik het adres en het nummer, en verder niets.",
  "Ik was op zoek naar {termen} hier in de buurt. Jullie staan in de gids, maar een eigen site kon ik nergens vinden.",
 ],
 'weg': [
  "Ik keek naar {termen} in de regio en kwam bij jullie uit. Je domein {domein} bestaat nog, alleen staat er niets meer op.",
  "Bij jullie kwam ik een webadres tegen dat nergens meer heen gaat. {domein} bestaat, de site is weg.",
  "Ik wilde jullie site bekijken. {domein} doet het niet meer, op geen van de manieren waarop ik het geprobeerd heb.",
 ],
 'mobiel': [
  "Ik heb {domein} op mijn telefoon geopend, want daar kijkt je klant. Op een laptop is er weinig aan de hand, op een telefoon loopt hij over de rand.",
  "Je site opende ik op mijn telefoon. Daar gaat iets mis dat je op een laptop niet ziet.",
  "Op {domein} viel me iets op, maar pas toen ik hem op mijn telefoon opende.",
 ],
 'lek': [
  "Ik heb {domein} bekeken zoals iemand dat doet die jullie nodig heeft. Hij werkt, alleen kwam ik er op het laatst net niet doorheen.",
  "Je site doet het en ziet er verzorgd uit. Toch strandde ik bij het stukje van kijken naar bellen.",
  "Ik keek op {domein} en liep vast op iets kleins dat je zelf nooit tegenkomt.",
 ],
 'portaal': [
  "Ik kwam jullie tegen op een leadportaal en wilde daarna je eigen site zien. Die is er niet.",
  "Op het portaal staan jullie er goed op. Daarbuiten kon ik jullie nergens vinden.",
 ],
 'kring': [
  "Ik liep de ledenlijst van de Bedrijvenkring langs en klikte op jullie naam. Er zit geen site achter.",
  "Jullie staan bij de Bedrijvenkring, met adres en nummer. Een link naar een eigen site ontbreekt.",
 ],
 'vak': [
  "Ik zag op {domein} dat jullie meer doen dan er op de site staat.",
  "Op je site staat het werk van een paar jaar geleden, terwijl jullie inmiddels verder zijn.",
 ],
}
SLOT = [
 "Er viel me meer op. Daar heb ik een pagina over gemaakt. Scan de code hiernaast, dan neem ik je erin mee.",
 "Wat me verder opviel heb ik op een pagina gezet. Scan de code, dan laat ik het je zien.",
 "De rest heb ik voor je uitgewerkt op een eigen pagina. Scan de code hiernaast, dan neem ik je erin mee.",
 "Ik heb er een pagina over gemaakt. Scan de code, dan loop ik het met je langs.",
]
TERM = {'installatie': 'installatiebedrijven', 'elektro': 'elektrotechnische bedrijven',
        'bouw': 'aannemers', 'afbouw': 'afbouwbedrijven', 'metaal': 'metaalbedrijven',
        'grond': 'grondverzetbedrijven', 'techniek': 'technische bedrijven'}

def splits_adres(a):
    m = re.match(r'^(.*?[^\d\s])\s+(\d+)\s*(.*)$', (a or '').strip())
    if not m: return (a or '').strip(), '', ''
    return m.group(1).strip(), m.group(2), m.group(3).strip(' -')

def main():
    idx = {r['slug']: r for r in csv.DictReader(open('/Users/simonkempers/Desktop/Pique - B2B Appointment Intelligence/Klanten/BCS/onlinegeduld/_index.csv', encoding='utf-8'))}
    fb = {r['bedrijf']: r for r in csv.DictReader(open(os.path.join(MAP, 'Online-Geduld-FaseB-Batch50.csv'), encoding='utf-8'))}

    KOP = ['voornaam','achternaam','aanhef','straatnaam','huisnummer','toevoeging','postcode',
           'plaatsnaam','land','brieftekst','link','unieke_url','functie','bedrijf',
           'beslisser_bron','beslisser_status','notitie']
    rijen, geen_naam, adresvlag = [], 0, 0

    for slug, i in idx.items():
        r = fb[i['bedrijf']]
        dom = re.sub(r'^https?://', '', (r.get('website') or '')).split('/')[0].replace('www.', '')
        sub = dict(plaats=r['plaats'], domein=dom,
                   termen=TERM.get(r['branche'], 'bedrijven'),
                   url=f"{BASIS}/{slug}")
        tekst = (kies(OPENING[i['pad']], i['bedrijf'], 'op').format(**sub) + "\n\n"
                 + kies(SLOT, i['bedrijf'], 'sl') + "\n\n" + AFZENDER)

        # beslisser
        vn = (r.get('voornaam') or '').strip()
        an = (r.get('achternaam') or '').strip()
        aanhef = f"Hoi {vn}" if vn else ''
        if vn:
            status, bronn = 'GEVERIFIEERD', r['beslisser_bron']
            notitie = f"Persoonlijk t.a.v. {vn} {an}"
            vol = (r.get('volledige_naam') or '').strip()
            if r.get('roepnaam_bron') == 'TE BEVESTIGEN':
                notitie += f" | register: {vol}. Roepnaam bevestigen aan de telefoon"
            elif r.get('roepnaam_bron') == 'roepnaam staat in de handelsnaam':
                notitie += f" | roepnaam uit de handelsnaam, register: {vol}"
        else:
            status, bronn = 'ONOPGELOST', ''
            notitie = "Brief + naam volgt: eigenaar"
            geen_naam += 1

        straat, nr, toev = splits_adres(r['adres'])
        pc = r['postcode']
        pc = f"{pc[:4]} {pc[4:]}" if re.fullmatch(r'\d{4}[A-Z]{2}', pc) else pc
        if 'bevestigd' not in r['bag_status']:
            notitie += " | ADRES DUBBELCHECKEN: niet bevestigd bij de BAG"; adresvlag += 1

        rijen.append(dict(voornaam=vn, achternaam=an, aanhef=aanhef, straatnaam=straat,
            huisnummer=nr, toevoeging=toev, postcode=pc, plaatsnaam=r['plaats'], land='Nederland',
            brieftekst=tekst, link=f"https://{BASIS}/{slug}", unieke_url=f"onlinegeduld/{slug}",
            functie=(r.get('rol') or 'Eigenaar'), bedrijf=i['bedrijf'], beslisser_bron=bronn,
            beslisser_status=status, notitie=notitie))

    uit = os.path.join(MAP, 'Online-Geduld-Brieven-VERZENDKLAAR.csv')
    with open(uit, 'w', newline='\n', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=KOP, quoting=csv.QUOTE_ALL); w.writeheader(); w.writerows(rijen)

    # ── verplichte controles ─────────────────────────────────────────
    print(f"{len(rijen)} rijen geschreven naar {os.path.basename(uit)}\n")
    fout = 0
    def toets(naam, ok, extra=''):
        nonlocal fout
        print(f"  {'ok  ' if ok else 'FOUT'}  {naam} {extra}")
        if not ok: fout += 1

    gelezen = list(csv.DictReader(open(uit, encoding='utf-8')))
    toets("17 kolommen op elke rij", all(len(x) == 17 for x in gelezen))
    toets("koppen in canonieke volgorde", list(gelezen[0].keys()) == KOP)
    toets("geen dubbele unieke_url", len({x['unieke_url'] for x in gelezen}) == len(gelezen))
    toets("basis + unieke_url is de link",
          all(x['link'] == 'https://intro-pique.agency/' + x['unieke_url'] for x in gelezen))
    toets("aanhef begint met 'Hoi ' waar een voornaam is",
          all((x['aanhef'].startswith('Hoi ') if x['voornaam'] else x['aanhef'] == '') for x in gelezen))
    toets("geen 'Hoi ' in de brieftekst", not any('Hoi ' in x['brieftekst'] for x in gelezen))
    toets("geen 'Groet' in de brieftekst", not any('Groet' in x['brieftekst'] for x in gelezen))
    n_sig = sum(1 for x in gelezen if x['brieftekst'].rstrip().endswith('\n' + AFZENDER))
    toets("elke brief eindigt op de voornaam van de afzender", n_sig == len(gelezen), f"({n_sig}/{len(gelezen)})")
    # Bewuste afwijking van regel 5c uit de brieven-csv-agent: het adres staat niet op
    # de kaart, want intro-pique.agency zegt de ontvanger van een kaart van Cheraldo
    # niets. De QR is hier de enige route, dus die moet kloppen.
    n_adr = sum(1 for x in gelezen if 'intro-pique' in x['brieftekst'] or 'http' in x['brieftekst'])
    toets("geen webadres in de brieftekst, alleen de QR", n_adr == 0, f"({n_adr} met adres)")
    toets("geen geruststelling over de code",
          not any(re.search(r'geen spam|veilig|betrouwbaar|gerust', x['brieftekst'], re.I) for x in gelezen))
    toets("geen zin die begint met Niet/Geen/Juist/Precies",
          not any(re.search(r'(?m)(?:^|(?<=[.!?]\s))(Niet|Geen|Juist|Precies)\b', x['brieftekst']) for x in gelezen))
    toets("geen 'niet X, maar Y'",
          not any(re.search(r'\bniet\b[^.\n]{2,60}\bmaar\b|\bgeen\b[^.\n]{2,60}\bmaar\b', x['brieftekst'], re.I) for x in gelezen))
    toets("geen em-dash, puntkomma of emoji",
          not any(re.search(r'[—;\U0001F300-\U0001FAFF]', x['brieftekst']) for x in gelezen))
    toets("geen wij-vorm", not any(re.search(r'\b(wij|we) (zagen|helpen|vonden)\b', x['brieftekst'], re.I) for x in gelezen))
    wc = [len(x['brieftekst'].split()) for x in gelezen]
    toets("elke kaart onder de 50 woorden", max(wc) < 50, f"(langste {max(wc)}, gemiddeld {sum(wc)//len(wc)})")
    toets("elke rij heeft een adres", all(x['straatnaam'] and x['huisnummer'] and x['postcode'] for x in gelezen))

    print(f"\n  zonder voornaam op de kaart: {geen_naam}")
    print(f"  adresvlaggen: {adresvlag}")
    print(f"  onopgeloste beslissers: {sum(1 for x in gelezen if x['beslisser_status'] == 'ONOPGELOST')}")
    print(f"\n{'ALLES SCHOON' if fout == 0 else str(fout) + ' CONTROLES GEZAKT'}")

main()
