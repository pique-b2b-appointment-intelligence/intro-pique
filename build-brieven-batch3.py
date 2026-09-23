#!/usr/bin/env python3
# Bouwt de handgeschreven-brieven CSV voor franchise batch 3.
import csv, json, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SP = "/private/tmp/claude-501/-Users-simonkempers-Desktop-Pique---B2B-Appointment-Intelligence/cf61064a-4c50-4f1d-9295-495fa487c304/scratchpad"
meta = json.load(open(os.path.join(SP, "b3-meta.json"), encoding="utf-8"))

ORG = {
 "profile-tyrecenter":"Profile Tyrecenter","euromaster":"Euromaster","vakgarage":"Vakgarage",
 "bosch-car-service":"Bosch Car Service","kwik-fit":"Kwik-Fit","olympia":"Olympia","continu":"Continu",
 "luba":"Luba","timing":"Timing","csu":"CSU","asito":"Asito","trigion":"Trigion","krinkels":"Krinkels",
 "idverde":"idverde","nvd-beveiliging":"NVD Beveiliging","boels":"Boels Rental","colle":"Collé Rental & Sales",
 "ooms":"Ooms Makelaars","van-der-sande":"Van der Sande Makelaars","rodenburg":"Rodenburg Bedrijfsmakelaars",
 "van-dorp":"Van Dorp","breman":"Breman Installatiegroep","kuijpers":"Kuijpers","hoppenbrouwers":"Hoppenbrouwers Techniek",
 "unica":"Unica","eriks":"ERIKS","oosterberg":"Oosterberg","rensa":"Rensa","rubix":"Rubix Nederland",
 "fabory":"Fabory","cws":"CWS Nederland","blycolin":"Blycolin","rentex":"Rentex","maas-international":"Maas International",
 "peeze":"Peeze","esdec":"Esdec","libra-energy":"Libra Energy","rovc":"ROVC","ncoi":"NCOI Opleidingen",
 "schouten-nelissen":"Schouten & Nelissen","uts":"UTS Nederland","simon-loos":"Simon Loos","probo":"Probo",
 "drukwerkdeal":"Drukwerkdeal","vegro":"Vegro","harting-bank":"Harting-Bank","countus":"Countus","aaff":"aaff",
}

# adres per slug: [straat, huisnr, toevoeging, postcode, plaats]
ADDR = {
 "profile-tyrecenter":["Citadel","14","","3905 NK","Veenendaal"],
 "euromaster":["Lübeckstraat","2","","7418 EC","Deventer"],
 "vakgarage":["Melkrijder","15","","3861 SG","Nijkerk"],
 "bosch-car-service":["Ringwade","31","A","3439 LM","Nieuwegein"],
 "kwik-fit":["Daltonstraat","17","","3846 BX","Harderwijk"],
 "olympia":["Mercuriusplein","1","","2132 HA","Hoofddorp"],
 "continu":["Flight Forum","40","","5657 DB","Eindhoven"],
 "luba":["Eschertoren","1","A","2316 ET","Leiden"],
 "timing":["Deventerstraat","15","2","7311 BH","Apeldoorn"],
 "csu":["Verlengde Velmolen","1","","5406 NT","Uden"],
 "asito":["Van Riemsdijkplein","50","","7606 ZA","Almelo"],
 "trigion":["Karel Doormanweg","4","","3115 JD","Schiedam"],
 "krinkels":["Rithsestraat","87","","4813 GW","Breda"],
 "idverde":["Rijksweg","11","","5076 PB","Haaren"],
 "nvd-beveiliging":["Delftlaan","325","","2024 CH","Haarlem"],
 "boels":["Dr. Nolenslaan","140","","6136 GV","Sittard"],
 "colle":["Nusterweg","100-102","","6136 KV","Sittard"],
 "ooms":["Maaskade","113","","3071 NJ","Rotterdam"],
 "van-der-sande":["Vijverstraat","1","","4818 ST","Breda"],
 "rodenburg":["Paslaan","20","","7311 AL","Apeldoorn"],
 "van-dorp":["Koraalrood","161","","2718 SB","Zoetermeer"],
 "breman":["Sasdijk","9","","8281 BM","Genemuiden"],
 "kuijpers":["Panovenweg","18","","5708 HR","Helmond"],
 "hoppenbrouwers":["Kreitenmolenstraat","201","","5071 ND","Udenhout"],
 "unica":["De Wel","15","","3871 MT","Hoevelaken"],
 "eriks":["Toermalijnstraat","5","","1812 RL","Alkmaar"],
 "oosterberg":["IJsseldijk","2","","7325 WZ","Apeldoorn"],
 "rensa":["Bedrijvenweg","10","","7007 CE","Doetinchem"],
 "rubix":["Ekkersrijt","6040","","5692 GA","Son en Breugel"],
 "fabory":["Laurent Janssensstraat","112","","5048 AR","Tilburg"],
 "cws":["De Beverspijken","16","","5221 ED","'s-Hertogenbosch"],
 "blycolin":["Heksekamp","33","","5301 LX","Zaltbommel"],
 "rentex":["Koopman Heeresweg","2","","8701 PR","Bolsward"],
 "maas-international":["Science Park Eindhoven","5051","","5692 EB","Son en Breugel"],
 "peeze":["Ringoven","36","","6826 TR","Arnhem"],
 "esdec":["Londenstraat","16","","7418 EE","Deventer"],
 "libra-energy":["Eendrachtstraat","199","","1951 AX","Velsen-Noord"],
 "rovc":["Galvanistraat","13","","6716 AE","Ede"],
 "ncoi":["Marathon","7","","1213 PD","Hilversum"],
 "schouten-nelissen":["Van Heemstraweg West","5","","5301 PA","Zaltbommel"],
 "uts":["Donau","90","","2491 BC","Den Haag"],
 "simon-loos":["Tender","2","","1687 JB","Wognum"],
 "probo":["Fortuinweg","17","","9101 PE","Dokkum"],
 "drukwerkdeal":["Keulenstraat","4","","7418 ET","Deventer"],
 "vegro":["Vennestraat","13","","2161 LE","Lisse"],
 "harting-bank":["Atoomweg","111","","3542 AB","Utrecht"],
 "countus":["Dokter Stolteweg","2","","8025 AV","Zwolle"],
 "aaff":["Agro Business Park","85","","6708 PV","Wageningen"],
}

ORDER = list(ORG.keys())
cols = ["voornaam","achternaam","aanhef","straatnaam","huisnummer","toevoeging","postcode","plaatsnaam","land",
        "brieftekst","link","unieke_url","functie","bedrijf","beslisser_bron","beslisser_status","notitie"]

def slot(org): return f"Ik ben daarna nog wat dieper in {org} gedoken. Wat me is opgevallen heb ik voor je uitgeschreven. Scan de QR-code hiernaast, dan neem ik je erin mee."

rows=[]; warn=[]
for s in ORDER:
    m=meta[s]; org=ORG[s]; a=ADDR[s]
    vn=m["vn"]; an=m["an"]; status=m["status"]
    aanhef = f"Hoi {vn}" if vn else "Hoi"
    brief = m["obs"].strip() + "\n\n" + slot(org)
    wc=len(brief.split())
    if wc>52: warn.append(f"{s}: {wc} woorden")
    if status.startswith("waarschijnlijk"): notitie="Beslisser via deep research (LinkedIn/pers); vluchtig checken kan"
    else: notitie=""
    if m.get("note"): notitie=(notitie+". " if notitie else "")+m["note"]
    rows.append({
        "voornaam":vn,"achternaam":an,"aanhef":aanhef,
        "straatnaam":a[0],"huisnummer":a[1],"toevoeging":a[2],"postcode":a[3],"plaatsnaam":a[4],"land":"Nederland",
        "brieftekst":brief,"link":f"https://intro-pique.agency/pique/{s}","unieke_url":f"pique/{s}",
        "functie":m["functie"],"bedrijf":org,"beslisser_bron":"Fase B-verificatie (zie Pique-Franchise-Batch3-FaseB-Verificatie.md)",
        "beslisser_status":status,"notitie":notitie,
    })

out=os.path.join(HERE,"Pique-Franchise-Batch3-Brieven.csv")
with open(out,"w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
    for r in rows: w.writerow(r)

# Kopie naar de Outreach-map
folder=glob.glob(os.path.join(HERE,"../../Marketing/Outreach/*Franchise - 9 juli - ca. 50 stuks"))[0]
import shutil; shutil.copyfile(out, os.path.join(folder,"Pique-Franchise-Batch3-Brieven.csv"))

byst={}
for r in rows: byst[r["beslisser_status"]]=byst.get(r["beslisser_status"],0)+1
print(f"CSV klaar: {len(rows)} rijen -> {os.path.basename(out)} (+ kopie in Outreach-map)")
print("status:", byst)
print("lange kaarten (>52 woorden):", warn or "geen")
PY = None
