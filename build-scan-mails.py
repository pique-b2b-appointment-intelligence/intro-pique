#!/usr/bin/env python3
# Bouwt de opvolgmails (na QR-scan) voor de franchise-prospects. Zonder "zonder verkoopverhaal".
import csv

# vn, an, bedrijf, functie, email, conf, bron, hook, note, scans
P = [
 ("Mark","Hendriksen","Abemec","Commercieel Manager","mark.hendriksen@abemec.nl","PATROON","abemec.nl/contact (formaat voornaam.achternaam, ~80%)",
  "hoe elke vestiging zijn eigen agrarische klanten binnenhaalt","Adres geconstrueerd uit geverifieerd bedrijfsformaat; niet 1-op-1 bevestigd.",1),
 ("Annet","Kosse","Atalian Nederland","Salesmanager","Annet.Kosse@atalianworld.com","PATROON","atalianworld.com (formaat Voornaam.Achternaam, bevestigd via 2 echte adressen)",
  "hoe nieuwe schoonmaak- en facilitaire contracten per regio binnenkomen","Personeelsmail via atalianworld.com (niet atalian.nl). Adres geconstrueerd uit bevestigd formaat.",2),
 ("Gerald","Merkus","OBN Ongedierte Bestrijding Nederland","Directeur","gerald@obn.eu","PATROON","obn.eu/contact (formaat voornaam@)",
  "hoe elke vestiging zijn eigen klanten in de regio wint","Officieel domein is obn.eu (niet obn.nl). Adres geconstrueerd uit bedrijfsformaat.",1),
 ("Joris","Janssen","Glaspunt","Marketing Manager / mede-aandeelhouder","joris@glas.nl","PATROON","glas.nl/contact (formaat voornaam@, 100%)",
  "hoe elke vestiging zijn lokale opdrachten binnenhaalt","glaspunt.nl leidt door naar glas.nl (het echte maildomein). Adres geconstrueerd uit bedrijfsformaat.",1),
 ("Rianne","van Koot","Gio Coffee","Teamlead Marketing","rianne.vankoot@giocoffee.nl","PATROON","giocoffee.nl (formaat voornaam.achternaam)",
  "hoe nieuwe zakelijke koffieklanten per regio binnenkomen","Eigen site toont alleen info@. Alternatief: rianne.koot@giocoffee.nl.",1),
 ("Emiel","de Bruin","TSNed (Traffic Service Nederland)","Algemeen Directeur","emieldebruin@tsned.nl","PATROON","tsned.nl/contact (formaat voornaamachternaam aaneen, bevestigd via echte adressen)",
  "hoe jullie per regio nieuwe opdrachtgevers vinden","Formaat hard afgeleid van echte medewerkeradressen op de eigen site.",1),
 ("Lisanne","de Gier-Valken","Oranjedak","Management Assistent","l.degier@oranjedak.nl","PATROON","oranjedak.nl (formaat voorletter.achternaam, ~94%, bevestigd via a.schrauwen@/e.stevenaar@)",
  "hoe elke vestiging zijn eigen dakopdrachten binnenhaalt","Gecorrigeerd na bounce (was voornaam.achternaam). Alt bij bounce: l.gier@ of ldegier@oranjedak.nl.",1),
 ("Peet","Ceelen","Kemkens","Hoofd Verkoop","peet.ceelen@kemkens.nl","PATROON","kemkens.nl/contact (formaat voornaam.achternaam)",
  "hoe elke vestiging zijn klanten in de regio wint","Eigen site toont alleen verkoop@/klantenservice@. Adres geconstrueerd uit bedrijfsformaat.",1),
 ("Walter","van der Velden Jonkers","Van der Velden Rioleringsbeheer","Business Unit Directeur","walter.vanderveldenjonkers@vandervelden.com","PATROON","vandervelden.com (formaat voornaam.achternaam, volledige familienaam aaneen; bevestigd via marleen.delaat@)",
  "hoe nieuwe opdrachtgevers per regio bij jullie terechtkomen","Gecorrigeerd na bounce (Jonkers ontbrak). Alt: walter.jonkers@ of w.vanderveldenjonkers@vandervelden.com.",1),
 ("Daan","van der Veen","Dutch Quality Gardens","Voorzitter coöperatie","","GEEN","dutchqualitygardens.nl/contact",
  "hoe de aangesloten hoveniers per regio aan nieuwe opdrachten komen","GEEN persoonlijk adres: heeft geen eigen bedrijf meer, coöperatie voert enkel info@. daan@ bouncte. Bellen: 085-222 0392. Speculatieve gok: daan@dqghoveniers.nl.",1),
 ("Marcel","de Waal","Mondial Movers","Algemeen Directeur","marcel@mondial-movers.nl","GOK","mondial-movers.nl/contact",
  "hoe de grote zakelijke verhuizingen per aangesloten verhuizer binnenkomen","Domein met koppelteken. Voornaam@-adres, onbevestigd. Bounce = bellen. Alt: m.dewaal@ of mdewaal@.",1),
 ("Rebecca","Koelemeijer","Nedflex","Sales Manager Franchise & White Label","r.koelemeijer@nedflex.nl","GEVONDEN","nedflex.nl/dit-zijn-wij (direct adres op teampagina)",
  "hoe nieuwe white-label- en franchisepartners binnenkomen","Direct adres van de eigen teampagina.",1),
]

# Korte, natuurlijke bedrijfsnaam in de mailtekst
DISPLAY = {
 "Abemec":"Abemec","Atalian Nederland":"Atalian","OBN Ongedierte Bestrijding Nederland":"OBN",
 "Glaspunt":"Glaspunt","Gio Coffee":"Gio Coffee","TSNed (Traffic Service Nederland)":"TSNed",
 "Oranjedak":"Oranjedak","Kemkens":"Kemkens","Van der Velden Rioleringsbeheer":"Van der Velden",
 "Dutch Quality Gardens":"Dutch Quality Gardens","Mondial Movers":"Mondial Movers","Nedflex":"Nedflex",
}

def mail(vn, bedrijf, hook, scans):
    disp = DISPLAY.get(bedrijf, bedrijf)
    keek = "de pagina zelfs een paar keer hebt bekeken" if scans>1 else "de pagina hebt bekeken"
    return (f"Hoi {vn},\n\n"
            f"Ik stuurde je laatst een handgeschreven kaart met een QR-code. Ik zag dat je 'm hebt gescand en {keek}. Leuk, daar werd ik nieuwsgierig van.\n\n"
            f"Die pagina maakte ik voor {disp} omdat me iets opviel: {hook}. Daar zou ik het graag eens kort met je over hebben.\n\n"
            f"Zullen we een keer vijftien minuten bellen? Dan laat ik zien wat ik precies bedoel. Komt bellen niet uit, dan hoor ik het gewoon.\n\n"
            f"Groet,\nSimon")

cols=["voornaam","achternaam","bedrijf","functie","email","email_confidence","email_bron","onderwerp","mailtekst","notitie"]
rows=[]
for vn,an,bedrijf,functie,email,conf,bron,hook,note,scans in P:
    rows.append({"voornaam":vn,"achternaam":an,"bedrijf":bedrijf,"functie":functie,"email":email,
                 "email_confidence":conf,"email_bron":bron,"onderwerp":f"Je keek even, {vn}",
                 "mailtekst":mail(vn,bedrijf,hook,scans),"notitie":note})

with open("Pique-Franchise-Scan-Mails.csv","w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); [w.writerow(r) for r in rows]

assert not any("verkoopverhaal" in r["mailtekst"] for r in rows), "verkoopverhaal nog aanwezig!"
print(f"{len(rows)} mails herbouwd. 'verkoopverhaal' aanwezig: NEE")
