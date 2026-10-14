#!/usr/bin/env python3
"""Bouwt de Buiten-Goed-pagina's uit _sjabloon.html plus de inhoud per prospect.

De vorm zit in het sjabloon, de copy komt uit inhoud/<slug>.json. Die splitsing is
geen netheid maar een regel uit CLAUDE.md: copy die in een bouwbestand wordt getypt
levert sjabloontaal op, en dat is precies waar zeven eerdere LP-versies op sneuvelden.
Dit script schrijft dus niets en vult alleen in.

    python3 bouw-lp.py                # bouwt alles waarvoor inhoud klaarstaat
    python3 bouw-lp.py --lijst        # toont wat er nog aan inhoud ontbreekt
"""
import argparse, csv, html, json, os, re, sys, unicodedata
from urllib.parse import quote

HIER = os.path.dirname(os.path.abspath(__file__))
LIJST = os.path.join(HIER, '..', '..', 'Lightr', 'BuitenGoed', 'Buiten-Goed-Prospectlijst.csv')
WOORD = {1: 'Eén', 2: 'Twee', 3: 'Drie'}
VOORZET = {'van', 'de', 'der', 'den', 'ten', 'ter', 'te', 'het', 'la', 'le', 'du', 'di'}


def slug(naam):
    s = unicodedata.normalize('NFKD', naam).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\b(b\.?v\.?|v\.?o\.?f\.?|n\.?v\.?)\b', ' ', s)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return re.sub(r'-+', '-', s)


def voornaam(beslisser):
    b = re.sub(r'\s*\(.*?\)\s*', '', beslisser).strip()
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


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--lijst', action='store_true')
    n = a.parse_args()

    sjabloon = open(os.path.join(HIER, '_sjabloon.html'), encoding='utf-8').read()
    rijen = list(csv.DictReader(open(LIJST, encoding='utf-8-sig')))

    klaar, open_nog, urls = 0, [], []
    for r in rijen:
        bedrijf, sl = r['Bedrijf'].strip(), slug(r['Bedrijf'])
        pad = os.path.join(HIER, 'inhoud', sl + '.json')
        if not os.path.exists(pad):
            open_nog.append(f'{sl}.json  ({bedrijf})')
            continue
        c = json.load(open(pad, encoding='utf-8'))
        vn = c.get('voornaam') or voornaam(r['Beslisser'])
        if not vn:
            print(f'  GEEN VOORNAAM, overgeslagen: {bedrijf}', file=sys.stderr)
            continue
        bev = c['bevindingen']
        v = {
            'BEDRIJF': html.escape(bedrijf),
            'BEDRIJF_JS': bedrijf.replace("'", "\\'"),
            'BEDRIJF_URL': quote(bedrijf),
            'VOORNAAM': html.escape(vn),
            'VOORNAAM_JS': vn.replace("'", "\\'"),
            'AANTAL': str(len(bev[:3])),
            'AANTAL_WOORD': WOORD[len(bev[:3])].lower(),
            'AANTAL_WOORD_HOOFD': WOORD[len(bev[:3])],
            'DOSSIER': dossierblok(bev),
            'WAAROMJIJ': html.escape(c['waarom_jij']),
            'WATDIT_ONDERWERP': html.escape(c['watdit_onderwerp']),
            'PIVOT': html.escape(c['pivot']),
            'BETEKENT_KOP': html.escape(c['betekent_kop']),
            'BETEKENT': c['betekent'],          # mag <strong> bevatten
            'PULL': html.escape(c['pull']),
            'VOORSTEL': html.escape(c['voorstel']),
        }
        uit = sjabloon
        for k, w in v.items():
            uit = uit.replace('{{' + k + '}}', w)
        rest = re.findall(r'\{\{([A-Z_]+)\}\}', uit)
        if rest:
            print(f'  NIET INGEVULD in {sl}: {sorted(set(rest))}', file=sys.stderr)
            continue
        open(os.path.join(HIER, sl + '.html'), 'w', encoding='utf-8').write(uit)
        urls.append({'bedrijf': bedrijf, 'beslisser': r['Beslisser'],
                     'url': f'https://evenkennismaken.nl/buiten-goed/{sl}',
                     'bestand': sl + '.html'})
        klaar += 1

    if n.lijst or open_nog:
        print(f'{len(open_nog)} prospects wachten nog op inhoud:', file=sys.stderr)
        for o in open_nog[:100]:
            print('   ' + o, file=sys.stderr)
    if n.lijst:
        return
    if urls:
        with open(os.path.join(HIER, 'Buiten-Goed-LP-URLs.csv'), 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.DictWriter(f, fieldnames=['bedrijf', 'beslisser', 'url', 'bestand'])
            w.writeheader(); w.writerows(urls)
    print(f'{klaar} pagina\'s gebouwd', file=sys.stderr)


if __name__ == '__main__':
    main()
