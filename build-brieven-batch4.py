#!/usr/bin/env python3
# Bouwt de handgeschreven-kaart CSV voor de nieuwe-100 franchise batch (79 prospects).
import csv, json, os

SP = "/private/tmp/claude-501/-Users-simonkempers-Desktop-Pique---B2B-Appointment-Intelligence/cf61064a-4c50-4f1d-9295-495fa487c304/scratchpad"
HERE = os.path.dirname(os.path.abspath(__file__))

master = json.load(open(os.path.join(SP, "np-master.json"), encoding="utf-8"))

# Adressen samenvoegen uit de drie onderzochte groepen.
ADDR = {}
for f in ["np/addr-125.json", "np/addr-3468.json", "np/addr-7.json"]:
    for a in json.load(open(os.path.join(SP, f), encoding="utf-8")):
        ADDR[a["slug"]] = a

# Persoonlijke kaart-hook per slug (2 zinnen, gegrond in de aanleiding).
HOOK = {
 "technische-unie":"Jullie bedienen installateurs en industrie vanuit een landelijk vestigingennet. De grote klant die net over de regiogrens zit, komt daar alleen niet vanzelf uit.",
 "novon":"Jullie schoonmaakcontracten worden per regio gewonnen, met personeelsbeleid als sterk verhaal. De opdrachtgever die daar het meest voor openstaat, hoort dat alleen niet vanzelf.",
 "vve-diensten":"Jullie groeien met regiokantoren die elk hun eigen VvE's binnenhalen. Het bestuur dat net buiten een kantoor valt, komt daar alleen niet vanzelf bij.",
 "netwerk-notarissen":"Jullie formule maakt losse kantoren samen sterk. De cliënt die per regio nog nergens zit, komt daar alleen niet vanzelf uit.",
 "asn-autoschade":"Na de overname door AAGB draait de franchise-integratie op volle toeren. Het herstelbedrijf of wagenpark dat per regio nog openstaat, komt daar alleen niet vanzelf bij.",
 "nmg-vastgoed":"Drie divisies, en het beheerwerk komt per regio binnen. De VvE of eigenaar die net buiten beeld zit, komt daar alleen niet vanzelf uit.",
 "damstra":"Vierde generatie, en jullie breiden uit met nieuwe vestigingen. De installatieklant die net over de regiogrens zit, komt daar alleen niet vanzelf bij.",
 "flanderijn":"Met een nieuwe directievoorzitter beweegt de koers, en opdrachtgevers komen per vestiging binnen. De partij die net buiten een regio valt, komt daar alleen niet vanzelf uit.",
 "mourik":"Sinds kort een nieuwe CEO, en het werk loopt over meerdere divisies en regio's. De opdrachtgever die het hele concern zou passen, spreekt daar alleen niemand van jullie gericht aan.",
 "goos-horeca":"Negen cash-and-carry's, elk met eigen horecaklanten in de buurt. De zaak die net buiten een vestiging valt, komt daar alleen niet vanzelf bij.",
 "taxatie-netwerk":"Jullie nieuwe funderingsmodel is precies waar de markt op zit te wachten. De opdrachtgever die dat het hardst nodig heeft, hoort er via vijftig losse taxateurs alleen niet vanzelf van.",
 "itn-groep":"Van Zeeuws familiebedrijf naar totaalinstallateur, dat bouw je niet in een jaar. De opdrachtgever die het hele gebouw bij één partij wil, komt daar per sector alleen niet vanzelf uit.",
 "bierens":"Incasso over de grens, met vestigingen in meerdere landen. De internationale opdrachtgever die de hele groep zou passen, komt daar alleen niet vanzelf bij.",
 "first-stop":"Jullie werven nieuwe partners en de centra draaien elk hun eigen wagenparken. Het contract dat net buiten een centrum valt, komt daar alleen niet vanzelf uit.",
 "1box":"Derde speler van Nederland, en particulieren vinden jullie vanzelf. De zakelijke huurder met structurele ruimtevraag komt daar alleen niet vanzelf bij.",
 "laadpaaldirect":"Ruim twintigduizend laadpunten, en de vraag blijft groeien. De VvE of het bedrijf met een groot project komt via losse installateurs alleen niet vanzelf bij de juiste beslisser.",
 "donker-groep":"Met Queisen erbij wordt jullie speelveld groter, niet vanzelf overzichtelijker. De aanbesteding die net over een regiogrens ligt, komt daar alleen niet vanzelf uit.",
 "arbo-unie":"Een nieuwe koers en een frisse naam op komst, met dertig vestigingen eronder. De grote werkgever die daar het beste past, hoort dat alleen niet vanzelf.",
 "beko":"Vier distributiecentra, elk met een eigen verkoopteam en eigen bakkers. De groeiende bakkerij die net buiten een route valt, komt daar alleen niet vanzelf bij.",
 "eurobox":"Een familiebedrijf dat blijft openen, en elke nieuwe locatie moet snel vol. De zakelijke huurder die daarvoor zorgt, komt daar alleen niet vanzelf bij.",
 "vink":"Jullie maken vaart met de online kant van de groothandel. Het maakbedrijf dat per regio nog nergens koopt, komt daar alleen niet vanzelf uit.",
 "feenstra":"De verduurzaming zorgt voor drukte, en de zakelijke kant loopt per vestiging. De corporatie of beheerder die net buiten beeld zit, komt daar alleen niet vanzelf bij.",
 "gkb":"Na de directiewissel staat er een nieuwe fase klaar, met overheidswerk per regio. De gemeente die net over de grens zit, komt daar alleen niet vanzelf uit.",
 "zorg-van-de-zaak":"Meer dan twintig labels onder één dak, en een werkgever raakt vaak maar één ervan. De klant die bij meerdere labels zou passen, komt daar alleen niet vanzelf uit.",
 "bunzl":"Met een nieuwe GM staat er een frisse koers, en horeca komt per regio binnen. De keten die nieuwe zaken opent, komt daar alleen niet vanzelf bij.",
 "bmn":"Midden in de rebrand, en de bouwers komen per vestiging binnen. De aannemer die net begint en nog nergens koopt, komt daar alleen niet vanzelf bij.",
 "cleanlease":"Met een nieuw MT staat er een nieuwe richting, en klanten komen per wasserij binnen. De zorggroep die net buiten een verzorgingsgebied valt, komt daar alleen niet vanzelf uit.",
 "preventief":"De aangescherpte BHV-regels brengen meer werkgevers dan ooit, per centrum. De grote werkgever met meerdere locaties komt daar alleen niet vanzelf bij.",
 "wasco":"Met de Rexel-integratie en elektra erbij verandert jullie bereik. De installateur die net overstapt, komt via losse vestigingen alleen niet vanzelf bij jullie.",
 "alpina":"Met alle overnames groeit jullie netwerk hard, elk kantoor met eigen klanten. De ondernemer die over meerdere regio's zit, komt daar alleen niet vanzelf uit.",
 "imk":"Met NL Sales Academy erbij draaien jullie opleidingen op meer locaties. De werkgever die net tussen twee locaties valt, komt daar alleen niet vanzelf bij.",
 "stiho":"Meerdere merken en vestigingen, en nu ook een duurzaamheidsverhaal. De aannemer die daar het meest voor openstaat, hoort het per vestiging alleen niet vanzelf.",
 "van-mossel":"De overnamereeks zette jullie op ruim honderd vestigingen. Het wagenpark dat net op de grens tussen twee vestigingen zit, komt daar alleen niet vanzelf uit.",
 "carel-lurvink":"Jullie bouwen nieuw, met klanten in schoonmaak, zorg en horeca. De instelling die klaar is om over te stappen, komt daar per regio alleen niet vanzelf bij.",
 "van-wijhe-verf":"De biobased lijn is precies waar een schilder warm voor loopt. De vakman die er het meest voor openstaat, hoort het via een verdeeld kanaal alleen niet vanzelf.",
 "pirtek":"Jullie werven franchisenemers en draaien zestien centers, elk in eigen regio. Het machinebedrijf dat nog geen vast contract heeft, komt daar alleen niet vanzelf bij.",
 "etl":"Met de buy-and-build staan jullie op ruim veertig kantoren met eigen mkb-klanten. De ondernemer die net over de grens zit, komt daar alleen niet vanzelf uit.",
 "select-windows":"Jullie werven partners en breiden het showroomnetwerk uit. De klant die aan nieuwe kozijnen toe is, komt per gebied alleen niet vanzelf bij de juiste partner.",
 "de-groot-installatiegroep":"Net een commercieel directeur erbij, en jullie doen installatie en brandbeveiliging. De klant die beide bij één partij wil, wordt per regio alleen niet vanzelf opgezocht.",
 "bidfood":"Horeca en instellingen komen binnen via regionale distributiecentra. De keuken die nog niet bij jullie bestelt, komt per DC alleen niet vanzelf in beeld.",
 "ambiance-zonwering":"Er komen nieuwe vestigingen bij onder jullie vlag, elk met een eigen verkoopgebied. De aanvraag die net buiten een vestiging valt, komt daar alleen niet vanzelf bij.",
 "sonepar":"Jullie bedienen installateurs vanuit een landelijk vestigingennet. De installateur die net verhuist of begint, kiest snel zijn groothandel, en komt daar alleen niet vanzelf bij jullie.",
 "peinemann":"Zeventig jaar en twaalf bedrijven onder één dak. De industrieklant die er maar één van kent, komt bij de rest alleen niet vanzelf uit.",
 "urban-care":"Groeien door overnames gaat snel, twintig kantoren samenbrengen kost jaren. De VvE die net buiten een regio valt, komt daar alleen niet vanzelf bij.",
 "solar-nederland":"Met het nieuwe XL-format in Heerenveen wordt jullie vestigingennet juist belangrijker. De installateur rond een nieuwe vestiging komt daar alleen niet vanzelf bij.",
 "premio":"Het netwerk groeit, en jullie zoeken zowel vestigingen als wagenparken. De fleetmanager komt niet naar de balie, en dus per vestiging alleen niet vanzelf in beeld.",
 "zeelandia":"Met de directiewissels kijk je opnieuw hoe je bakkers bereikt. De bakker die op het punt van kiezen staat, komt per regio alleen niet vanzelf in beeld.",
 "sanidrome":"Een formule van zelfstandige installateurs groeit met nieuwe leden. De sterke installateur die zou passen, meldt zich alleen niet vanzelf.",
 "mcb":"One-stop-shop voor de maakindustrie werkt alleen als de juiste inkoper het weet. Het maakbedrijf dat perfect past, komt per vestiging alleen niet vanzelf in beeld.",
 "pius-floris":"Jullie zoeken een commercieel manager en het aantal vestigingen groeit. De gemeente of beslisser achter een meerjarencontract komt per vestiging alleen niet vanzelf bij.",
 "sonneveld":"Jullie richten de commerciële kant opnieuw in. De bakker of keten die daar het meest toe doet, komt per regio alleen niet vanzelf in beeld.",
 "paardekooper":"Veel labels en vestigingen onder één groep, elk met eigen klanten. De grote regionale klant die bij meerdere labels past, komt daar alleen niet vanzelf uit.",
 "copijn":"Met een nieuwe algemeen directeur kijk je opnieuw naar hoe projecten binnenkomen. Het project dat het langst stil blijft, komt per regio alleen niet vanzelf bij.",
 "bouwmaat":"Rond de tweehonderd vestigingen die zichzelf vullen, met een nieuwe directeur sinds januari. Het grote bouwbedrijf dat bij meerdere zou passen, komt daar alleen niet vanzelf uit.",
 "lavans":"Jullie groeien de kant van cleanroom en food op, met abonnementen per regio. De specialistische klant die daar past, komt alleen niet vanzelf in beeld.",
 "pontmeyer":"Tweeenvijftig vestigingen en sinds het voorjaar een nieuwe directeur. Het bouwbedrijf dat bij meerdere vestigingen past, komt daar alleen niet vanzelf uit.",
 "batenburg":"Verduurzaming en laadlogistiek zitten in de lift, en jullie pakken je deel met zes vestigingen. Het meerjarencontract dat net over een regiogrens ligt, komt daar alleen niet vanzelf bij.",
 "orona":"Met de overname van UP en Elite komt er flink wat servicewerk en nieuwe klanten bij. De beheerder die tussen twee teams valt, komt daar alleen niet vanzelf uit.",
 "kroon-kozijn":"Vijftig jaar, eigen fabriek en vijfentwintig dealers met showroom. De aanvraag die bij een te drukke dealer blijft liggen, komt daar alleen niet vanzelf uit.",
 "schadenet":"De schadeherstelmarkt consolideert, en jullie zitten er met honderdtwintig locaties middenin. Het wagenpark dat bij meerdere locaties past, komt daar alleen niet vanzelf bij.",
 "rexel":"Met een nieuwe directie en veertig verkooppunten wil je grip op wie de regio's najagen. De industrieklant die net niet bereikt werd, komt daar alleen niet vanzelf uit.",
 "reym":"Onder REMONDIS wil je laten zien dat het netwerk als geheel presteert. De fabriek die net op de grens van twee werkgebieden zit, komt daar alleen niet vanzelf uit.",
 "autotaalglas":"Vierenvijftig vestigingen, dus er zit er altijd een om de hoek. Het landelijke wagenpark dat één aanspreekpunt wil, komt daar via losse vestigingen alleen niet vanzelf uit.",
 "sunmaster":"Een dealernetwerk van specialisten die elk hun eigen regio bedienen. Het grote zakelijke project dat het hele land raakt, komt daar alleen niet vanzelf uit.",
 "anticimex":"Na de overname van Traas bedienen acht vestigingen elk hun eigen klanten. De landelijke aanbesteding die één antwoord vraagt, komt daar alleen niet vanzelf uit.",
 "arboned":"Met ruim veertig locaties zit je dicht op het mkb in elke regio. De werkgever met meerdere vestigingen komt daar alleen niet vanzelf uit.",
 "autofirst":"Met ruim honderdnegentig vestigingen groeit AutoFirst harder dan het overzicht. Het landelijke wagenpark dat één partner wil, komt daar alleen niet vanzelf uit.",
 "van-leeuwen":"Met de commerciële rol vacant vraag ik me af wie het geheel overziet. Het grote project dat over meerdere regio's loopt, komt daar alleen niet vanzelf uit.",
 "sortimo":"Jullie richten bedrijfswagens in via Centers door het land. Het landelijke wagenpark dat overal dezelfde inrichting wil, komt daar alleen niet vanzelf uit.",
 "top-movers":"Zestien verhuizers over vijfentwintig vestigingen, met de stap naar zero-emissie. De organisatie die meerdere kantoren tegelijk verhuist, komt daar alleen niet vanzelf uit.",
 "mastermate":"Zeven familiebedrijven, één naam, eenendertig vestigingen. De commerciële motor die per lid anders draait, komt centraal alleen niet vanzelf in beeld.",
 "bott":"Jullie werken via partners, en of de fleetmanager je product ziet hangt van de regio af. De fleet die net nieuwe wagens bestelt, komt daar alleen niet vanzelf bij.",
 "koelweb":"Jullie serviceteam rijdt het hele land door, maar contracten worden per regio gewonnen. De food-locatie die je nog niet benadert, komt daar alleen niet vanzelf bij.",
 "selecta":"Een druk servicenet voelt als groei, maar zegt niets over nieuwe kantoren. De facilitair beslisser op het aanbestedingsmoment komt daar alleen niet vanzelf bij.",
 "elis":"Elf locaties die in eigen regio nieuwe klanten binnenhalen naast de operatie. Het bedrijf dat nu bij een ander wast, komt daar alleen niet vanzelf uit.",
 "truckland":"Dertien vestigingen en meerdere merken, elk met eigen transportklanten. De fleet die aan vervanging toe is, komt daar alleen niet vanzelf bij de juiste vestiging.",
 "bruns":"Jullie leven van projecten met een lange, stille aanloop. Het museum dat nu in stilte plannen maakt, komt daar alleen niet vanzelf bij jullie in beeld.",
 "directveilig":"Gegroeid naar acht vestigingen die elk mkb-klanten binnenhalen. Het bedrijf dat nu een beveiligingskeuze maakt, komt daar alleen niet vanzelf bij.",
 "van-losser":"Met Krechting erbij komt er weer een regio en een klantenbestand bij. De vestiging die na de overname moet blijven groeien, doet dat alleen niet vanzelf.",
}

SLOT = "\n\nIk ben daarna nog wat dieper in {org} gedoken. Wat me is opgevallen heb ik voor je uitgeschreven. Scan de QR-code hiernaast, dan neem ik je erin mee."

rows = []
missing_addr = []
for m in master:
    s = m["slug"]
    a = ADDR.get(s, {})
    if not a.get("straatnaam"):
        missing_addr.append(m["org"])
    brief = HOOK[s] + SLOT.format(org=m["org"])
    rows.append({
        "voornaam": m["vn"], "achternaam": "", "aanhef": f"Hoi {m['vn']}",
        "straatnaam": a.get("straatnaam", ""), "huisnummer": a.get("huisnummer", ""),
        "toevoeging": a.get("toevoeging", ""), "postcode": a.get("postcode", ""),
        "plaatsnaam": a.get("plaatsnaam", ""), "land": "Nederland",
        "brieftekst": brief, "link": f"https://intro-pique.agency/pique/{s}",
        "unieke_url": f"pique/{s}", "functie": m["functie"], "bedrijf": m["org"],
        "beslisser_bron": "nieuwe-100 beslisser-verificatie (57 hard / 23 LinkedIn)",
        "beslisser_status": "bevestigd", "notitie": "adres nog invullen" if not a.get("straatnaam") else "",
    })

cols = ["voornaam","achternaam","aanhef","straatnaam","huisnummer","toevoeging","postcode",
        "plaatsnaam","land","brieftekst","link","unieke_url","functie","bedrijf",
        "beslisser_bron","beslisser_status","notitie"]
out = os.path.join(HERE, "Pique-Franchise-Nieuw100-Brieven.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow(r)

print(f"CSV klaar: {len(rows)} kaarten -> {out}")
print(f"Adres ontbreekt ({len(missing_addr)}): {', '.join(missing_addr) if missing_addr else 'geen'}")
