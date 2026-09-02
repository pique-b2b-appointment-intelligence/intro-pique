#!/usr/bin/env python3
"""Haalt de volledige naam van de bestuurder uit het contactblok van drimble.

Het handelsregister toont via companyinfo alleen de initiaal. Drimble publiceert
per vestiging een contactblok met Voornaam, Achternaam en Titelnaam. De URL is te
bouwen uit het vestigingsnummer dat companyinfo al meelevert.

Staan er meerdere contacten, dan wint degene wiens initiaal past bij de bestuurder
uit het handelsregister. Zo raak je bij een V.O.F. niet de verkeerde vennoot.
"""
import csv, re, sys, unicodedata, html as H
from concurrent.futures import ThreadPoolExecutor
import requests, urllib3, time, threading
urllib3.disable_warnings()
_REM=threading.Lock(); _L=[0.0]
PAUZE=1.4
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                 '(KHTML, like Gecko) Chrome/126.0 Safari/537.36'}
CONTACT=re.compile(r'Voornaam:\s*([A-Z][\w\'\-]{1,20}(?:\s+[A-Z][\w\'\-]{1,20}){0,3})\s*'
                   r'Achternaam:\s*((?:van|de|den|der|te|ten|op)?\s*[A-Z][\w\'\-\s]{1,30}?)\s*'
                   r'Titelnaam:\s*([A-Za-z\s]{3,30}?)\s*E-mail')
def sl(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',s)).strip('-')

def een(x):
    for k in ('d_voornaam','d_achternaam','d_rol','d_url','d_alle'): x[k]=''
    kvk=x.get('ci_kvk') or x.get('kvk_nummer') or ''
    if '-' not in kvk: return x
    vest=kvk.split('-')[1].lstrip('0')
    naam=x.get('eindklant') or x.get('bedrijf')
    pl=x.get('plaats') or x.get('ci_plaats') or ''
    u=f"https://drimble.nl/bedrijf/{sl(pl)}/{vest}/{sl(naam)}.html"
    try:
        with _REM:
            w=PAUZE-(time.time()-_L[0])
            if w>0: time.sleep(w)
            _L[0]=time.time()
        r=requests.get(u,headers=UA,timeout=20,verify=False)
        if r.status_code!=200: return x
        t=re.sub(r'\s+',' ',H.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'(?is)<(script|style).*?</\1>','',r.text))))
        if naam.split()[0].lower() not in t.lower()[:4000]: return x
        best=(x.get('ci_bestuurder') or x.get('kvk_bestuurder') or '')
        ach=best.split(',')[0].strip().lower()
        init=best.split(',')[-1].strip().rstrip('.').lower() if ',' in best else ''
        kand=[]
        for m in CONTACT.finditer(t):
            vn,an,rol=m.group(1).strip(),m.group(2).strip(),m.group(3).strip()
            if 'BBBB' in vn or 'BBBB' in an: continue
            kand.append((vn,an,rol))
        if not kand: return x
        x['d_alle']=' | '.join(f"{a} {b} ({c})" for a,b,c in kand)
        # eerst op initiaal, dan op achternaam, dan de eerste
        keuze=None
        for vn,an,rol in kand:
            if init and vn[:1].lower()==init[:1] and (not ach or ach.split()[-1] in an.lower()):
                keuze=(vn,an,rol); break
        if not keuze and ach:
            keuze=next(((v,a,r2) for v,a,r2 in kand if ach.split()[-1] in a.lower()), None)
        keuze=keuze or kand[0]
        x['d_voornaam'],x['d_achternaam'],x['d_rol'],x['d_url']=keuze[0],keuze[1],keuze[2],u
    except Exception: pass
    return x

rijen=list(csv.DictReader(open(sys.argv[1],encoding='utf-8')))
doen=[x for x in rijen if '-' in (x.get('ci_kvk') or x.get('kvk_nummer') or '')]
print(f"{len(doen)} bedrijven met een vestigingsnummer")
with ThreadPoolExecutor(max_workers=3) as ex:
    for i,_ in enumerate(ex.map(een,doen),1):
        if i%25==0: print(f'  {i}/{len(doen)}',flush=True)
for x in rijen:
    for k in ('d_voornaam','d_achternaam','d_rol','d_url','d_alle'): x.setdefault(k,'')
raak=sum(1 for x in rijen if x['d_voornaam'])
print(f"\nvolledige naam bij {raak} van de {len(doen)}")
with open(sys.argv[2],'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rijen[0].keys())); w.writeheader(); w.writerows(rijen)
