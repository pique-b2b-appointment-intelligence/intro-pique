#!/usr/bin/env python3
"""Bouwt de The System-pagina's uit _sjabloon.html plus de inhoud per prospect.

De vorm zit in het sjabloon, de copy komt uit inhoud/<slug>.json. Die splitsing is
geen netheid maar een regel uit CLAUDE.md: copy die in een bouwbestand wordt getypt
levert sjabloontaal op, en daar sneuvelden zeven eerdere LP-versies op. Dit script
schrijft dus niets en vult alleen in.

    python3 bouw-lp.py                # bouwt alles waarvoor inhoud klaarstaat
    python3 bouw-lp.py --lijst        # toont wat er nog aan inhoud ontbreekt

De prospectlijst is Klanten/The-System/prospectlijst.csv, dezelfde lijst die Maarten
in het portaal nakijkt. Een bedrijf dat daar niet meer op staat krijgt dus ook geen
pagina, en dat is de bedoeling.
"""
import argparse
import csv
import html
import json
import os
import re
import sys
import unicodedata
from urllib.parse import quote

HIER = os.path.dirname(os.path.abspath(__file__))
LIJST = os.path.join(HIER, '..', '..', 'The-System', 'prospectlijst.csv')
WOORD = {1: 'Eén', 2: 'Twee', 3: 'Drie'}
VOORZET = {'van', 'de', 'der', 'den', 'ten', 'ter', 'te', 'het', 'la', 'le', 'du', 'di'}


def slug(naam):
    s = unicodedata.normalize('NFKD', naam).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\b(b\.?v\.?|v\.?o\.?f\.?|n\.?v\.?)\b', ' ', s)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return re.sub(r'-+', '-', s)


def kortenaam(naam):
    """De rechtsvorm eraf voor de lopende tekst.

    'Ik keek een tijd naar Markhorst Elektro B.V.' leest als een uittreksel. In de
    kaart, de aanhef en de chips staat daarom de naam zoals iemand hem uitspreekt;
    de titel en de mailregel houden de volledige naam.
    """
    return re.sub(r'(?i)\s*\b(b\.?v\.?|n\.?v\.?|v\.?o\.?f\.?|c\.?v\.?)\.?\s*$', '', naam).strip()


def voornaam(beslisser):
    """Alleen een echte voornaam. Initialen leveren 'Hé W.' op en dat is erger dan niets.

    Zeventien van de 200 beslissers staan op een initiaal, zie
    feedback_prospectlijst_poorten. Die krijgen de kop zonder naam.
    """
    b = re.sub(r'(?i)^(dhr|mevr|mw|de heer|mevrouw)\.?\s*', '', beslisser or '').strip()
    b = re.sub(r'\s*\(.*?\)\s*', '', b).strip()
    d = b.split()
    if not d:
        return ''
    v = d[0].strip('.,')
    return '' if (len(v) <= 2 or v.lower() in VOORZET or '.' in d[0]) else v


def dossierblok(bevindingen):
    """Maximaal drie rijen: lp12.css kent transition-delays voor nth-child 1 tot en met 3."""
    uit = []
    for i, b in enumerate(bevindingen[:3], 1):
        hier = ' hier' if b.get('hier') else ''
        cit = ''
        if b.get('citaat'):
            cit = f'\n                <q class="dv-cit">{html.escape(b["citaat"])}</q>'
        uit.append(
            f'            <div class="dv-rij{hier}">\n'
            f'              <span class="dv-nr">{i:02d}</span>\n'
            f'              <div class="dv-kol">\n'
            f'                <span class="dv-wat">{html.escape(b["wat"])}</span>{cit}\n'
            f'                <span class="dv-bron"><i></i><b>{html.escape(b["bron"])}</b>'
            f' &middot; {html.escape(b["datum"])}</span>\n'
            f'              </div>\n'
            f'            </div>')
    return '\n'.join(uit)


def mechblok(stappen):
    """Welke stap een mens doet en welke een agent. Het label is de enige plek waar
    het gevulde accent terugkomt, want gevuld accent is voor actie."""
    uit = []
    for i, s in enumerate(stappen, 1):
        wie = 'agent' if s['wie'] == 'agent' else 'mens'
        label = 'De agent' if wie == 'agent' else 'Jullie'
        uit.append(
            f'      <li class="tsrij {wie}" style="transition-delay:{0.06 * i:.2f}s">'
            f'<span class="vul" aria-hidden="true" style="transition-delay:{0.06 * i + 0.1:.2f}s"></span>'
            f'<span class="st">{i:02d}</span>'
            f'<span class="wa">{html.escape(s["wat"])}</span>'
            f'<span class="wi">{label}</span></li>')
    return '\n'.join(uit)


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--lijst', action='store_true')
    n = a.parse_args()

    sjabloon = open(os.path.join(HIER, '_sjabloon.html'), encoding='utf-8').read()
    rijen = list(csv.DictReader(open(LIJST, encoding='utf-8-sig')))

    klaar, open_nog, urls = 0, [], []
    for r in rijen:
        bedrijf, sl = r['bedrijf'].strip(), slug(r['bedrijf'])
        pad = os.path.join(HIER, 'inhoud', sl + '.json')
        if not os.path.exists(pad):
            open_nog.append(f'{sl}.json  ({bedrijf})')
            continue
        c = json.load(open(pad, encoding='utf-8'))
        vn = c.get('voornaam') or voornaam(r['beslisser'])
        bev = c['bevindingen']
        # Zonder voornaam vervalt de naam uit de kop, zie reference_lp_vaste_koppen.
        v = {
            'BEDRIJF': html.escape(bedrijf),
            'BEDRIJF_KORT': html.escape(c.get('bedrijf_kort') or kortenaam(bedrijf)),
            'BEDRIJF_KORT_JS': (c.get('bedrijf_kort') or kortenaam(bedrijf)).replace("'", "\\'"),
            'BEDRIJF_JS': bedrijf.replace("'", "\\'"),
            'BEDRIJF_URL': quote(bedrijf),
            'VOORNAAM': html.escape(vn),
            'VOORNAAM_JS': vn.replace("'", "\\'"),
            'AANTAL': str(len(bev[:3])),
            'AANTAL_WOORD': WOORD[len(bev[:3])].lower(),
            'AANTAL_WOORD_HOOFD': WOORD[len(bev[:3])],
            'DOSSIER': dossierblok(bev),
            'HERO_SUB': html.escape(c['hero_sub']),
            'WAAROMJIJ': html.escape(c['waarom_jij']),
            'WATDIT_ONDERWERP': html.escape(c['watdit_onderwerp']),
            'PIVOT': html.escape(c['pivot']),
            'BETEKENT_KOP': html.escape(c['betekent_kop']),
            'BETEKENT': c['betekent'],          # mag <strong> bevatten
            'PULL': html.escape(c['pull']),
            'VOORSTEL': html.escape(c['voorstel']),
            'MECH_KOP': html.escape(c['mech_kop']),
            'MECH': mechblok(c['mech']),
            'MECH_AANTAL': str(len(c['mech'])),
            'AGENT_AANTAL': str(sum(1 for x in c['mech'] if x['wie'] == 'agent')),
            'CTA_SUB': html.escape(c['cta_sub']),
        }
        uit = sjabloon
        if not vn:
            uit = uit.replace('H&eacute; <span class="u">{{VOORNAAM}}</span>, dit is waarom',
                              'Dit is waarom')
            uit = uit.replace('Hoi {{VOORNAAM}}.<br>', '')
            uit = uit.replace("'Hoi {{VOORNAAM_JS}}.', ", '')
        for k, w in v.items():
            uit = uit.replace('{{' + k + '}}', w)
        rest = re.findall(r'\{\{([A-Z_]+)\}\}', uit)
        if rest:
            print(f'  NIET INGEVULD in {sl}: {sorted(set(rest))}', file=sys.stderr)
            continue
        open(os.path.join(HIER, sl + '.html'), 'w', encoding='utf-8').write(uit)
        urls.append({'bedrijf': bedrijf, 'beslisser': r['beslisser'],
                     'url': f'https://intro-pique.agency/thesystem/{sl}',
                     'bestand': sl + '.html'})
        klaar += 1

    if n.lijst:
        print(f'{len(open_nog)} prospects wachten nog op inhoud:', file=sys.stderr)
        for o in open_nog[:100]:
            print('   ' + o, file=sys.stderr)
        return
    if urls:
        with open(os.path.join(HIER, 'TheSystem-LP-URLs.csv'), 'w', newline='',
                  encoding='utf-8-sig') as f:
            w = csv.DictWriter(f, fieldnames=['bedrijf', 'beslisser', 'url', 'bestand'])
            w.writeheader()
            w.writerows(urls)
    print(f'{klaar} pagina\'s gebouwd, {len(open_nog)} wachten op inhoud', file=sys.stderr)


if __name__ == '__main__':
    main()
